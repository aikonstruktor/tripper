from langgraph.graph import StateGraph, MessagesState, START, END
from langchain.messages import AIMessage, HumanMessage
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from tools import add, subtract, multiply, divide
import os

load_dotenv()

SYSTEM_PROMPT = AIMessage("You are a helpful assistant with tools, use them to answer user questions")
TASK = HumanMessage("Calculate 6 times 7 and then add 8")

tools = [add, subtract, multiply, divide]
tools_node = ToolNode(tools)

llm = ChatGroq(model = os.getenv("GROQ_MODEL"),
		api_key = os.getenv("GROQ_API_KEY"),
		temperature = 0)
llm_with_tools = llm.bind_tools(tools)
def llm_node(state: MessagesState):
  conversation = [SYSTEM_PROMPT] + state["messages"]
  response = llm_with_tools.invoke(conversation)
  return {"messages": [response]}

graph = StateGraph(MessagesState)
graph.add_node("llm",llm_node)
graph.add_node("tools",tools_node)
graph.add_edge(START, "llm")
graph.add_conditional_edges("llm", tools_condition)
graph.add_edge("tools", "llm")
graph.add_edge("llm", END)

my_graph = graph.compile()
result = my_graph.invoke({"messages": [TASK]})
for m in result["messages"]:
  m.pretty_print()

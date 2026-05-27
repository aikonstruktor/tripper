from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient
from strands.models.openai import OpenAIModel
from dotenv import load_dotenv 
import os

# Create a system prompt that explains the calculator capabilities
SYSTEM_PROMPT = """
You are a helpful calculator assistant that can perform basic arithmetic operations.
You have access to the following calculator tools:
- add: Add two numbers together
- subtract: Subtract one number from another
- multiply: Multiply two numbers together
- divide: Divide one number by another

When asked to perform calculations, use the appropriate tool rather than calculating the result yourself.
Explain the calculation and show the result clearly.
"""


def get_model():
    model = OpenAIModel(
        client_args={
            "api_key": os.getenv("NVIDIA_API_KEY"),
            "base_url": os.getenv("NVIDIA_URL"),
        },
        model_id=os.getenv("NVIDIA_MODEL"),
        params={
            "max_tokens": 2000,
            "temperature": 0,
        }
    )
    return model

def get_agent(tools):
    # Initialize agent
    agent = Agent(
        model=get_model(),
        system_prompt=SYSTEM_PROMPT,
        tools=tools,
    )
    return agent

def create_streamable_http_transport():
    return streamablehttp_client("http://localhost:8000/mcp/")

def main():
    streamable_http_mcp_client = MCPClient(create_streamable_http_transport)
    with streamable_http_mcp_client:
        tools = streamable_http_mcp_client.list_tools_sync()
        print(f"Available MCP tools: {[tool.tool_name for tool in tools]}")
        agent = get_agent(tools)
        print("\nCalculator Agent Ready! Type 'exit' to quit.\n")
        while True:
            user_input = input("Question: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            print("\nThinking...\n")
            response = agent(user_input)
            print(f"Answer: {response}\n")


if __name__ == "__main__":
    try:
        load_dotenv()
        main()
    except KeyboardInterrupt:
        print("\nExiting...")

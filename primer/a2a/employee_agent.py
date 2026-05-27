import os
from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient
from strands.multiagent.a2a import A2AServer
from urllib.parse import urlparse
from strands.models.openai import OpenAIModel
from strands import tool
from dotenv import load_dotenv
from employee_data import SKILLS, EMPLOYEES


SYSTEM_PROMPT = "You are Employee Agent who answers questions about employees. you must abbreviate employee first names and list all their skills"
EMPLOYEE_MCP_URL = "http://localhost:8002/mcp/"
EMPLOYEE_AGENT_URL = "http://localhost:8001/"

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
        description="Employee Agent that answers questions about employees and their skills"
    )
    return agent

def create_streamable_http_transport():
    return streamablehttp_client(EMPLOYEE_MCP_URL)

@tool
def get_skills() -> set[str]:
    """all of the skills that employees may have - use this list to figure out related skills"""
    print("get_skills")
    return SKILLS

@tool
def get_employees_with_skill(skill: str) -> list[dict]:
    """employees that have a specified skill - output includes fullname (First Last) and their skills"""
    print(f"get_employees_with_skill({skill})")
    skill_lower = skill.lower()
    employees_with_skill = [employee for employee in EMPLOYEES if any(s.lower() == skill_lower for s in employee["skills"])]
    if not employees_with_skill:
        raise ValueError(f"No employees have the {skill} skill")
    return employees_with_skill

def mcp_main():
    load_dotenv()
    streamable_http_mcp_client = MCPClient(create_streamable_http_transport)
    with streamable_http_mcp_client:
        tools = streamable_http_mcp_client.list_tools_sync()
        print(f"Available MCP tools: {[tool.tool_name for tool in tools]}")
        employee_agent = get_agent(tools)
        a2a_server = A2AServer(
            agent=employee_agent, 
            host=urlparse(EMPLOYEE_AGENT_URL).hostname, 
            port=int(urlparse(EMPLOYEE_AGENT_URL).port),
        )
    a2a_server.serve(host="0.0.0.0", port=8001)

if __name__ == "__main__":
    load_dotenv()
    tools = [get_skills, get_employees_with_skill]
    employee_agent = get_agent(tools)
    a2a_server = A2AServer(
        agent=employee_agent, 
        host=urlparse(EMPLOYEE_AGENT_URL).hostname, 
        port=int(urlparse(EMPLOYEE_AGENT_URL).port),
    )
    a2a_server.serve(host="0.0.0.0", port=8001)
            

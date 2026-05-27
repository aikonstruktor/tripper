from strands import Agent
from strands.models.openai import OpenAIModel
from dotenv import load_dotenv
from strands.tools import tool
import os

load_dotenv()

# 1. Define Groq as the underlying model
groq_model = OpenAIModel(
    model_id=os.getenv("GROQ_MODEL"),  
    client_args={
        "api_key": os.getenv("GROQ_API_KEY"),
        "base_url": "https://api.groq.com/openai/v1"
    },
    params={"temperature": 0}
)

# 2. Define a custom tool
@tool
def check_server_status(server_id: str) -> str:
    """Checks the health and status of a specified server."""
    # Your tool logic here
    return f"Server {server_id} is operational."

# 3. Create the Agent
my_agent = Agent(
    model=groq_model,
    tools=[check_server_status],
    system_prompt="You are a DevOps analysis agent. Help troubleshoot infrastructure."
)

# Run the agent
my_agent("Can you check the status of server SVR-9021?")

from typing import Any, Dict

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
from dotenv import load_dotenv
load_dotenv()

class WebSafeLiteLlm(LiteLlm):
    """
    Dev-Server-safe wrapper around LiteLlm.
    Overrides serialization to prevent `adk web` from crashing on llm_client.
    """
    def model_dump(self, *args, **kwargs) -> Dict[str, Any]:
        return {
            "model": self.model,
            "type": "LiteLlm (Web Safe Workaround)"
        }

moviemcp = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params={
                "command": "npx", 
                "args": ["tmdb-mcp-server"],
                # "args": ["-y", "@cinetribe/mcp-server-tmdb@latest"],
                "env": {
                    # "TMDB_API_KEY": "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxZTYwY2M1ODhjOTU5NmQ4MjIzZDFlNWVkYmZkZGRhYSIsIm5iZiI6MTc3ODQwNjUyNi44MDA5OTk5LCJzdWIiOiI2YTAwNTQ3ZTVkM2RhZDUyZmFhOGQyOTAiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.j7L52JY62rlltIRGjDXeM6SaHj8UuLOwfpFQaQBgheI",
                     "TMDB_ACCESS_TOKEN": "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxZTYwY2M1ODhjOTU5NmQ4MjIzZDFlNWVkYmZkZGRhYSIsIm5iZiI6MTc3ODQwNjUyNi44MDA5OTk5LCJzdWIiOiI2YTAwNTQ3ZTVkM2RhZDUyZmFhOGQyOTAiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.j7L52JY62rlltIRGjDXeM6SaHj8UuLOwfpFQaQBgheI"
                }
                }
        ),
    )

root_agent = Agent(
    name="movie_assistant",
    # model=LiteLlm(model="huggingface/mistralai/Mistral-7B-Instruct-v0.2"),
    # model=WebSafeLiteLlm("meta/llama-3.1-70b-instruct"),
    # model=WebSafeLiteLlm("huggingface/meta-llama/Llama-3.1-70B-Instruct"),
    model = WebSafeLiteLlm(
        model="openai/meta/llama-3.1-70b-instruct", 
        api_key="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", # Your NVIDIA key
        api_base="https://integrate.api.nvidia.com/v1" # Your NVIDIA base URL
    ),
    # model=WebSafeLiteLlm(model="huggingface/openai/gpt-oss-120b",
    #     model_kwargs={
    #         "reasoning": False,
    #         "include_reasoning": False,
    #     }
    #     ),
    instruction="You are a helpful movie assistant. Use the tools provided to answer movie questions.",
    tools=[moviemcp]
)


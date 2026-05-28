from typing import Any, Dict

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

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

root_agent = Agent(
    name="groq_assistant",
    # model=LiteLlm(model="huggingface/mistralai/Mistral-7B-Instruct-v0.2"),
    model=WebSafeLiteLlm(model="groq/llama-3.1-8b-instant"),
    instruction="You are a helpful assistant, that answers user questions in minimal tokens."
)

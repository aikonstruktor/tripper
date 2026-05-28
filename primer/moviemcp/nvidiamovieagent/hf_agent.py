from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

root_agent = Agent(
    name="hf_assistant",
    # model=LiteLlm(model="huggingface/mistralai/Mistral-7B-Instruct-v0.2"),
    model=LiteLlm(model="huggingface/openai/gpt-oss-120b"),
    instruction="You are a helpful assistant powered by a Hugging Face model."
)

import os
from strands import Agent
from strands_tools import calculator
# from strands_nvidia_nim import NvidiaNIM
from strands.models.openai import OpenAIModel
from dotenv import load_dotenv
load_dotenv()

# model = NvidiaNIM(
#     api_key=os.getenv("NVIDIA_NIM_API_KEY"),
#     model_id="meta/llama-3.1-70b-instruct",
#     params={"max_tokens": 200, "temperature": 0}
# )

model = OpenAIModel(
    client_args={
        "api_key": os.getenv("NVIDIA_API_KEY"),
        "base_url": os.getenv("NVIDIA_URL"),
    },
    model_id=os.getenv("NVIDIA_MODEL"),
    params={
        "max_tokens": 200,
        "temperature": 0,
    }
)

agent = Agent(model=model, tools=[calculator])
agent("What is 123.456 * 789.012?")

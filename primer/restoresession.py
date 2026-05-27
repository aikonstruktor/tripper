import os
from pathlib import Path
import re
from dotenv import load_dotenv
from strands import Agent
from strands.models.openai import OpenAIModel
from strands.session.file_session_manager import FileSessionManager
from strands.agent.conversation_manager import SummarizingConversationManager

# constants
# Create sessions directory
SESSION_DIR = Path("./sessions")
SESSION_DIR.mkdir(exist_ok=True)
SESSION_ID = "demo_123"
# System prompt
SYSTEM_PROMPT = """
You are a helpful assistant that follows the user's instructions carefully.
"""

def get_model():
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
    return model

load_dotenv()

def get_session_manager():
    # Create session manager
    session_manager = FileSessionManager(
        session_id=SESSION_ID,
        storage_dir=str(SESSION_DIR)
    )
    return session_manager

def get_conversation_manager():
    # Create conversation manager
    conversation_manager = SummarizingConversationManager(
        summary_ratio=0.5,              # Summarize 50% of older messages
        preserve_recent_messages=3      # Ensures 3 most recent message pairs (user messages and agent responses) are always kept intact, without summarization
    )
    return conversation_manager

def debugger_callback_handler(**kwargs):
    # Print the values in kwargs so that we can see everything
    print(kwargs)

def get_agent():
    # Create agent with session and conversation management
    agent = Agent(
        system_prompt=SYSTEM_PROMPT,
        model=get_model(),
        conversation_manager=get_conversation_manager(),
        session_manager=get_session_manager(),
        # callback_handler=None,
        # state={"user_preferences": {"theme": "dark"}, "session_count": 0}
    )
    return agent

def main():
    agent = get_agent()
    agent_state = agent.state.get()
    print(f"Initial Agent State: {agent_state}")

    task = """
    What is my name and what are my hobbies?
    """
    result = agent(task)


if __name__ == "__main__":
    main()

from google.adk.agents import Agent
from google.adk.tools import google_search
# from datetime import datetime

# from google.adk.models.lite_llm import LiteLlm

# def get_current_time() -> dict:
#     """
#     Get the current time in the format YYYY-MM-DD HH:MM:SS
#     """
#     return {
#         "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     }

# MODEL_GPT = "openai/gpt-4o-mini"

root_agent = Agent(
    name="tool_agent",
    model="gemini-2.0-flash",
    # model=LiteLlm(model=MODEL_GPT),
    description="Tool agent",
    instruction="""
    You are a helpful assistant that can use the following tools:
    - google_search
    """,
    tools=[google_search],
    # tools=[get_current_time],
    # tools=[google_search, get_current_time], # <--- Doesn't work
)

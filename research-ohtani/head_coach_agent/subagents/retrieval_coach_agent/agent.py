"""

"""

from google.adk.agents.llm_agent import LlmAgent
from .tools import *

GEMINI_MODEL = "gemini-2.5-flash-lite"

retrieval_coach_agent = LlmAgent(
    name="retrieval_coach_agent",
    model=GEMINI_MODEL,
    description="",
    instruction="""
    """,
    tools=[],
    output_key="retrieval_data"
)
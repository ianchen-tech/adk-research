"""

"""

from google.adk.agents.llm_agent import LlmAgent
from .tools import *

GEMINI_MODEL = "gemini-2.5-flash-lite"

query_coach_agent = LlmAgent(
    name="query_coach_agent",
    model=GEMINI_MODEL,
    description="",
    instruction="""
    """,
    output_key="",
)
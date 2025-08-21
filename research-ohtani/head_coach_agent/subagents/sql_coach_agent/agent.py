"""

"""

from google.adk.agents.llm_agent import LlmAgent
from .tools import *

GEMINI_MODEL = "gemini-2.5-flash-lite"

sql_coach_agent = LlmAgent(
    name="sql_coach_agent",
    model=GEMINI_MODEL,
    description="",
    instruction="""
    """,
    output_key="",
)
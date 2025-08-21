"""

"""

from google.adk.agents import SequentialAgent, ParallelAgent, LoopAgent
from google.adk.tools.agent_tool import AgentTool

from .subagents.sql_coach_agent import sql_coach_agent
from .subagents.query_coach_agent import query_coach_agent
from .subagents.scout_coach_agent import scout_coach_agent
from .subagents.analytics_coach_agent import analytics_coach_agent

# --- 1. Create Loop Agent ---
data_coach_agent = LoopAgent(
    name="data_coach_agent",
    sub_agents=[sql_coach_agent, query_coach_agent],
)

# --- 2. Create Parallel Agent ---
reference_coach_agent = ParallelAgent(
    name="reference_coach_agent",
    sub_agents=[data_coach_agent],
    tools=[AgentTool(scout_coach_agent)]
)

# --- 3. Create Sequential Agent ---
root_agent = SequentialAgent(
    name="head_coach_agent",
    sub_agents=[reference_coach_agent, analytics_coach_agent],
)


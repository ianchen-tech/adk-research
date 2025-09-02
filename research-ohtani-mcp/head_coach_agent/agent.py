"""Head Coach Agent for Ohtani MCP

使用 MCP 方法替換原本的 RAG 實作，直接透過 MCP 工具查詢 SQLite 資料庫
"""

from google.adk.agents import SequentialAgent, ParallelAgent

from .subagents.scout_coach_agent import scout_coach_agent
from .subagents.analytics_coach_agent import analytics_coach_agent
from .subagents.data_coach_agent.agent import data_coach_agent

# --- 2. Create Parallel Agent ---
reference_coach_agent = ParallelAgent(
    name="reference_coach_agent",
    sub_agents=[scout_coach_agent, data_coach_agent]
)

# --- 3. Create Sequential Agent ---
head_coach_agent = SequentialAgent(
    name="head_coach_agent",
    sub_agents=[reference_coach_agent, analytics_coach_agent],
)
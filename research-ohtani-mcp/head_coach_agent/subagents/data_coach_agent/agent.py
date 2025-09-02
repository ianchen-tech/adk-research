from pathlib import Path
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from .prompt import DATA_COACH_MCP_PROMPT

# 重要：動態計算 server.py 腳本的絕對路徑
PATH_TO_MCP_SERVER_SCRIPT = str((Path(__file__).parent / "server.py").resolve())

# --- 1. Create MCP-based Data Coach Agent ---
data_coach_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="data_coach_agent",
    description="專門透過 MCP 工具查詢大谷翔平資料庫數據的代理",
    instruction=DATA_COACH_MCP_PROMPT,
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command="python3",
                args=[PATH_TO_MCP_SERVER_SCRIPT],
            )
        )
    ],
    output_key="query_data"
)
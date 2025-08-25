"""

"""

from typing import Any, Dict
from google.adk.tools.tool_context import ToolContext


def set_default_review_feedback(tool_context: ToolContext) -> None:
    """
    設置預設的審查回饋狀態。

    此函數將 review_feedback 狀態初始化為空字串，
    用於確保後續 sql_coach_agent 代理可正常執行代理。

    Args:
        tool_context: 工具執行的上下文

    Returns:
        None
    """
    tool_context.state["review_feedback"] = ""


def retrieve_schema_and_example(text: str) -> Dict[str, Any]:
    """
    根據使用者的問題，提供相關的 schema 及範例。

    Args:
        text: 使用者的問題，將此進行 embedding 並搜尋相關的 schema 及範例

    Returns:
        Dict[str, Any]: 包含以下內容的字典：
            - result: 'failed' 或 'success'
            - schema: schema 內容及說明
            - examples: sql 範例
    """

    return {
        "result": "success",
        "schema": """
```sql
CREATE TABLE batting_game_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recent_game_rank INTEGER,
    opponent TEXT,
    score TEXT,
    game_type TEXT,
    at_bats INTEGER,
    runs INTEGER,
    hits INTEGER,
    doubles INTEGER,
    triples INTEGER,
    home_runs INTEGER,
    rbis INTEGER,
    walks INTEGER,
    strikeouts INTEGER,
    stolen_bases INTEGER,
    caught_stealing INTEGER,
    batting_avg REAL,
    obp REAL,
    slg REAL,
    ops REAL
);
```
        """,
        "examples": """
```sql
-- 查看最近5場打擊表現
SELECT 
    recent_game_rank,
    opponent,
    at_bats,
    hits,
    home_runs,
    rbis,
    batting_avg,
    ops
FROM batting_game_logs 
ORDER BY recent_game_rank ASC 
LIMIT 5;
```
        """,
    }

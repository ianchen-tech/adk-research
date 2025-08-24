"""

"""

from google.adk.agents.llm_agent import LlmAgent
from .tools import execute_sql, exit_loop

GEMINI_MODEL = "gemini-2.5-flash-lite"

fetching_coach_agent = LlmAgent(
    name="fetching_coach_agent",
    model=GEMINI_MODEL,
    description="能夠執行 SQL 語句查詢 SQLite 數據庫，並根據查詢結果判斷是否符合用戶需求。",
    instruction="""
    你是一個專門執行 SQL 查詢並且 Review 查詢結果的代理，主要任務是：
    
    1. 使用 execute_sql 工具執行 {current_sql} 中的 SQL 語句
    2. 根據工具返回結果進行判斷：
       - 如果 result 為 "success"：
         * 檢查 data 欄位中的 CSV 格式數據是否符合使用者的問題需求
         * 如果符合需求：將完整的工具回覆內容（包含 result 和 data 欄位）直接放到 current_data，不做任何修改，然後呼叫 exit_loop 工具結束循環
         * 如果不符合需求：將完整的工具回覆內容直接放到 current_data，不做任何修改，但不要呼叫 exit_loop 工具
       - 如果 result 為 "failed"：
         * 將完整的工具回覆內容（包含 result 和 data 欄位）直接放到 current_data，不做任何修改
         * 不要呼叫 exit_loop 工具，讓上層代理處理錯誤
    
    重要注意事項：
    - 始終保持工具回覆的原始格式，包含 result 和 data 兩個欄位
    - 成功時 data 欄位包含 CSV 格式的查詢結果
    - 失敗時 data 欄位為 "error"，錯誤詳情會記錄在 tool_context.state["review_feedback"] 中
    - 只有在查詢成功且數據符合需求時才呼叫 exit_loop
    """,
    tools=[execute_sql, exit_loop],
    output_key="current_data",
)
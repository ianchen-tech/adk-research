"""

"""

from google.adk.agents.llm_agent import LlmAgent
from .tools import retrieve_schema_and_example

GEMINI_MODEL = "gemini-2.5-flash-lite"

retrieval_coach_agent = LlmAgent(
    name="retrieval_coach_agent",
    model=GEMINI_MODEL,
    description="專門負責檢索和提供資料庫 schema 及 SQL 查詢範例的代理，根據使用者問題提供相關的資料庫結構說明和查詢示例",
    instruction="""
    你是一個資料庫檢索專家，專門負責根據使用者的問題提供相關的資料庫 schema 和 SQL 查詢範例。
    
    當收到使用者的問題時，你需要：
    1. 使用 retrieve_schema_and_example 工具來獲取相關的資料庫 schema 和查詢範例
    2. 根據工具回傳的 result 狀態進行回覆：
       - 如果 result 值是 "failed"，直接回覆："檢索失敗"
       - 如果 result 值是 "success"，直接回覆 schema 和 examples 這兩個 key 的值，不要進行任何修飾、修改或加工
    
    回覆格式範例（當 result 為 "success" 時）：
    
    ```
    **資料庫結構：**
    {直接輸出 schema 的值}
    
    **查詢範例：**
    {直接輸出 examples 的值}
    ```
    
    請嚴格按照此格式回覆，不要添加任何額外的說明或修飾。
    """,
    tools=[retrieve_schema_and_example],
    output_key="retrieval_result"
)
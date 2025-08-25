"""

"""

from google.adk.agents.llm_agent import LlmAgent

GEMINI_MODEL = "gemini-2.5-flash"

sql_coach_agent = LlmAgent(
    name="sql_coach_agent",
    model=GEMINI_MODEL,
    description="專門負責分析使用者問題並生成對應 SQL 查詢的代理，根據檢索到的資料庫 schema 和範例來構建精確的 SQL 語句",
    instruction="""
    你是一個 SQL 查詢專家，專門負責根據使用者的問題和提供的資料庫資訊生成精確的 SQL 查詢。
    
    參考資訊：
    {retrieval_result}
    
    根據上述資料庫結構和查詢範例，分析使用者的問題並生成對應的 SQL 查詢語句。
    
    **重要警告：**
    - 你的回覆內容必須只包含純 SQL 查詢語句
    - 不要添加任何解釋、說明或額外文字
    - 不要使用 ``` 符號或任何程式碼區塊標記
    - 不要包含註解或說明文字
    - 只回覆可以直接執行的 SQL 語句
    
    範例回覆格式：
    SELECT * FROM batting_game_logs WHERE recent_game_rank = 1;

    以下是你可能執行過的錯誤:
    {review_feedback}
    """,
    output_key="current_sql"
)
"""LinkedIn 貼文審查器代理

此代理審查 LinkedIn 貼文的品質並提供回饋。
"""

from google.adk.agents.llm_agent import LlmAgent

from .tools import count_characters, exit_loop

# 常數
GEMINI_MODEL = "gemini-2.0-flash"

# 定義貼文審查器代理
post_reviewer = LlmAgent(
    name="PostReviewer",
    model=GEMINI_MODEL,
    instruction="""你是一個 LinkedIn 貼文品質審查員。

    你的任務是評估關於代理開發套件 (ADK) 的 LinkedIn 貼文品質。
    
    ## 評估流程
    1. 使用 count_characters 工具檢查貼文長度。
       直接將貼文文字傳遞給工具。
    
    2. 如果長度檢查失敗（工具結果為 "fail"），請提供具體回饋說明需要修正的內容。
       使用工具的訊息作為指導，但加入你自己的專業評論。
    
    3. 如果長度檢查通過，請根據以下標準評估貼文：
       - 必要元素：
         1. 提及 @aiwithbrandon
         2. 列出多項 ADK 功能（至少 4 項）
         3. 有明確的呼籲行動
         4. 包含實際應用
         5. 展現真誠的熱忱
       
       - 風格要求：
         1. 不使用表情符號
         2. 不使用主題標籤
         3. 專業語調
         4. 對話式風格
         5. 清晰簡潔的寫作
    
    ## 輸出指示
    如果貼文未通過上述任何檢查：
      - 返回簡潔、具體的改善回饋
      
    否則如果貼文滿足所有要求：
      - 呼叫 exit_loop 函數
      - 返回 "貼文滿足所有要求。退出精煉循環。"
      
    不要修飾你的回應。要麼提供改善回饋，要麼呼叫 exit_loop 並返回完成訊息。
    
    ## 要審查的貼文
    {current_post}
    """,
    description="Reviews post quality and provides feedback on what to improve or exits the loop if requirements are met",
    tools=[count_characters, exit_loop],
    output_key="review_feedback",
)

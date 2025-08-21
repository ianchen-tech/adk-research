"""
行動推薦代理

此代理負責根據潛在客戶驗證和評分結果推薦適當的下一步行動。
"""

from google.adk.agents import LlmAgent

# --- 常數 ---
GEMINI_MODEL = "gemini-2.0-flash"

# 建立推薦代理
action_recommender_agent = LlmAgent(
    name="ActionRecommenderAgent",
    model=GEMINI_MODEL,
    instruction="""您是行動推薦 AI。
    
    根據潛在客戶資訊和評分：
    
    - 對於無效潛在客戶：建議需要哪些額外資訊
    - 對於評分 1-3 的潛在客戶：建議培養行動（教育內容等）
    - 對於評分 4-7 的潛在客戶：建議資格審查行動（探索電話、需求評估）
    - 對於評分 8-10 的潛在客戶：建議銷售行動（演示、提案等）
    
    將您的回應格式化為對銷售團隊的完整建議。
    
    潛在客戶分數：
    {lead_score}

    潛在客戶驗證狀態：
    {validation_status}
    """,
    description="根據潛在客戶資格審查推薦下一步行動。",
    output_key="action_recommendation",
)

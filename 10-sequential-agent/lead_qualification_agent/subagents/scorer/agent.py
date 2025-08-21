"""
潛在客戶評分代理

此代理負責根據各種標準為潛在客戶的資格等級評分。
"""

from google.adk.agents import LlmAgent

# --- 常數 ---
GEMINI_MODEL = "gemini-2.0-flash"

# 建立評分代理
lead_scorer_agent = LlmAgent(
    name="LeadScorerAgent",
    model=GEMINI_MODEL,
    instruction="""您是潛在客戶評分 AI。
    
    分析潛在客戶資訊並根據以下標準分配 1-10 的資格分數：
    - 表達的需求（問題的緊急性/清晰度）
    - 決策權威
    - 預算指標
    - 時間表指標
    
    僅輸出數字分數和一句理由說明。
    
    輸出範例：'8: 具有明確預算和即時需求的決策者'
    輸出範例：'3: 模糊興趣，未提及時間表或預算'
    """,
    description="以 1-10 的等級為合格潛在客戶評分。",
    output_key="lead_score",
)

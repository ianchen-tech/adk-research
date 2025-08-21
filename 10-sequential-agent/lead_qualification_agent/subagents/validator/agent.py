"""
潛在客戶驗證代理

此代理負責驗證潛在客戶是否具有資格審查所需的所有必要資訊。
"""

from google.adk.agents import LlmAgent

# --- 常數 ---
GEMINI_MODEL = "gemini-2.0-flash"

# 建立驗證代理
lead_validator_agent = LlmAgent(
    name="LeadValidatorAgent",
    model=GEMINI_MODEL,
    instruction="""您是潛在客戶驗證 AI。
    
    檢查使用者提供的潛在客戶資訊，並判斷是否足夠完整以進行資格審查。
    完整的潛在客戶應包括：
    - 聯絡資訊（姓名、電子郵件或電話）
    - 某些興趣或需求的表示
    - 公司或背景資訊（如適用）
    
    僅輸出 'valid' 或 'invalid'，如果無效則提供單一原因。
    
    有效輸出範例：'valid'
    無效輸出範例：'invalid: missing contact information'
    """,
    description="驗證潛在客戶資訊的完整性。",
    output_key="validation_status",
)

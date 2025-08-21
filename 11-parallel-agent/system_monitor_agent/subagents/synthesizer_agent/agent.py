"""系統報告合成器代理

此代理負責合成來自其他代理的資訊
以建立全面的系統健康報告。
"""

from google.adk.agents import LlmAgent

# --- 常數 ---
GEMINI_MODEL = "gemini-2.0-flash"

# 系統報告合成器代理
system_report_synthesizer = LlmAgent(
    name="SystemReportSynthesizer",
    model=GEMINI_MODEL,
    instruction="""您是一個系統報告合成器。
    
    您的任務是透過結合以下資訊來建立全面的系統健康報告：
    - CPU 資訊：{cpu_info}
    - 記憶體資訊：{memory_info}
    - 磁碟資訊：{disk_info}
    
    建立格式良好的報告，包含：
    1. 頂部的執行摘要，包含整體系統健康狀態
    2. 每個元件的各自資訊部分
    3. 基於任何令人擔憂指標的建議
    
    使用 markdown 格式使報告易讀且專業。
    突出顯示任何令人擔憂的數值並提供實用建議。
    """,
    description="將所有系統資訊合成為全面報告",
)

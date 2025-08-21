"""CPU 資訊代理

此代理負責收集和分析 CPU 資訊。
"""

from google.adk.agents import LlmAgent

from .tools import get_cpu_info

# --- 常數 ---
GEMINI_MODEL = "gemini-2.0-flash"

# CPU 資訊代理
cpu_info_agent = LlmAgent(
    name="CpuInfoAgent",
    model=GEMINI_MODEL,
    instruction="""您是一個 CPU 資訊代理。
    
    當被要求提供系統資訊時，您應該：
    1. 使用 'get_cpu_info' 工具收集 CPU 資料
    2. 分析返回的字典資料
    3. 將此資訊格式化為系統報告的簡潔、清晰部分
    
    該工具將返回一個包含以下內容的字典：
    - result：核心 CPU 資訊
    - stats：關於 CPU 使用情況的關鍵統計資料
    - additional_info：資料收集的上下文
    
    將您的回應格式化為結構良好的報告部分，包含：
    - CPU 核心資訊（實體與邏輯）
    - CPU 使用統計
    - 任何效能問題（高使用率 > 80%）
    
    重要：您必須呼叫 get_cpu_info 工具。不要編造資訊。
    """,
    description="收集和分析 CPU 資訊",
    tools=[get_cpu_info],
    output_key="cpu_info",
)

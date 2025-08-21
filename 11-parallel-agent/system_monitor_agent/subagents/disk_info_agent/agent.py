"""磁碟資訊代理

此代理負責收集和分析磁碟資訊。
"""

from google.adk.agents import LlmAgent

from .tools import get_disk_info

# --- 常數 ---
GEMINI_MODEL = "gemini-2.0-flash"

# 磁碟資訊代理
disk_info_agent = LlmAgent(
    name="DiskInfoAgent",
    model=GEMINI_MODEL,
    instruction="""您是一個磁碟資訊代理。
    
    當被要求提供系統資訊時，您應該：
    1. 使用 'get_disk_info' 工具收集磁碟資料
    2. 分析返回的字典資料
    3. 將此資訊格式化為系統報告的簡潔、清晰部分
    
    該工具將返回一個包含以下內容的字典：
    - result：核心磁碟資訊，包括分割區
    - stats：關於儲存使用情況的關鍵統計資料
    - additional_info：資料收集的上下文
    
    將您的回應格式化為結構良好的報告部分，包含：
    - 分割區資訊
    - 儲存容量和使用情況
    - 任何儲存問題（高使用率 > 85%）
    
    重要：您必須呼叫 get_disk_info 工具。不要編造資訊。
    """,
    description="收集和分析磁碟資訊",
    tools=[get_disk_info],
    output_key="disk_info",
)

"""LinkedIn 貼文生成器代理

此代理在精煉前生成初始的 LinkedIn 貼文。
"""

from google.adk.agents.llm_agent import LlmAgent

# 常數
GEMINI_MODEL = "gemini-2.0-flash"

# 定義初始貼文生成器代理
initial_post_generator = LlmAgent(
    name="InitialPostGenerator",
    model=GEMINI_MODEL,
    instruction="""你是一個 LinkedIn 貼文生成器。

    你的任務是為 @aiwithbrandon 的代理開發套件 (ADK) 教學創建一篇 LinkedIn 貼文。
    
    ## 內容要求
    確保貼文包含：
    1. 對從教學中學習的興奮感
    2. 學到的 ADK 特定功能：
       - 基本代理實作 (basic-agent)
       - 工具整合 (tool-agent)
       - 使用 LiteLLM (litellm-agent)
       - 管理會話和記憶體
       - 持久儲存功能
       - 多代理編排
       - 有狀態多代理系統
       - 回調系統
       - 用於管道工作流程的順序代理
       - 用於並行操作的平行代理
       - 用於反覆精煉的循環代理
    3. 關於改善 AI 應用程式的簡短陳述
    4. 提及/標記 @aiwithbrandon
    5. 明確的連結呼籲行動
    
    ## 風格要求
    - 專業且對話式的語調
    - 1000-1500 字元之間
    - 不使用表情符號
    - 不使用主題標籤
    - 展現真誠的熱忱
    - 突出實際應用
    
    ## 輸出指示
    - 僅返回貼文內容
    - 不要添加格式標記或解釋
    """,
    description="生成初始 LinkedIn 貼文以開始精煉過程",
    output_key="current_post",
)

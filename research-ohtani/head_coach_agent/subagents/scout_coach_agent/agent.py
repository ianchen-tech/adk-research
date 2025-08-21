"""

"""

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search

GEMINI_MODEL = "gemini-2.5-flash-lite"

scout_coach_agent = LlmAgent(
    name="scout_coach_agent",
    model=GEMINI_MODEL,
    description="情蒐教練代理，專門進行運動員相關的情報蒐集與總結",
    instruction="""
    你是一個專業的情蒐助理，專門進行運動員相關的情報蒐集並提供總結報告。
    當被詢問關於運動員的資訊時，你應該使用 google_search 工具來蒐集相關情報。
    
    重要限制：
    - 你只能蒐集和分析與運動員相關的情報和資料
    - 不得蒐集或提供非運動員相關的內容
    - 專注於運動員的表現、轉會、傷病、訓練、潛力評估等相關情報
    """,
    tools=[google_search]
)
"""
具有最小回調的順序代理

此範例展示了一個潛在客戶資格審查管道，具有最小的
before_agent_callback，僅在開始時初始化狀態一次。
"""

from google.adk.agents import SequentialAgent

from .subagents.recommender import action_recommender_agent
from .subagents.scorer import lead_scorer_agent

# 匯入子代理
from .subagents.validator import lead_validator_agent

# 建立具有最小回調的順序代理
root_agent = SequentialAgent(
    name="LeadQualificationPipeline",
    sub_agents=[lead_validator_agent, lead_scorer_agent, action_recommender_agent],
    description="驗證、評分並為銷售潛在客戶推薦行動的管道",
)

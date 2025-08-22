"""LinkedIn 貼文生成器根代理

此模組定義了 LinkedIn 貼文生成應用程式的根代理。
它使用一個順序代理，包含初始貼文生成器和後續的精煉循環。
"""

from google.adk.agents import LoopAgent, SequentialAgent

from .subagents.post_generator import initial_post_generator
from .subagents.post_refiner import post_refiner
from .subagents.post_reviewer import post_reviewer

# 建立精煉循環代理
refinement_loop = LoopAgent(
    name="PostRefinementLoop",
    max_iterations=10,
    sub_agents=[
        post_reviewer,
        post_refiner,
    ],
    description="反覆審查和精煉 LinkedIn 貼文，直到滿足品質要求",
)

# 建立順序管道
root_agent = SequentialAgent(
    name="LinkedInPostGenerationPipeline",
    sub_agents=[
        initial_post_generator,  # 步驟 1：生成初始貼文
        refinement_loop,  # 步驟 2：在循環中審查和精煉
    ],
    description="透過反覆審查過程生成和精煉 LinkedIn 貼文",
)

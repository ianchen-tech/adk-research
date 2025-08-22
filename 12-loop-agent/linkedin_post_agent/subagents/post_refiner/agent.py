"""LinkedIn 貼文精煉器代理

此代理根據審查回饋精煉 LinkedIn 貼文。
"""

from google.adk.agents.llm_agent import LlmAgent

# 常數
GEMINI_MODEL = "gemini-2.0-flash"

# 定義貼文精煉器代理
post_refiner = LlmAgent(
    name="PostRefinerAgent",
    model=GEMINI_MODEL,
    instruction="""You are a LinkedIn Post Refiner.

    Your task is to refine a LinkedIn post based on review feedback.
    
    ## INPUTS
    **Current Post:**
    {current_post}
    
    **Review Feedback:**
    {review_feedback}
    
    ## TASK
    Carefully apply the feedback to improve the post.
    - Maintain the original tone and theme of the post
    - Ensure all content requirements are met:
      1. Excitement about learning from the tutorial
      2. Specific aspects of ADK learned (at least 4)
      3. Brief statement about improving AI applications
      4. Mention/tag of @aiwithbrandon
      5. Clear call-to-action for connections
    - Adhere to style requirements:
      - Professional and conversational tone
      - Between 1000-1500 characters
      - NO emojis
      - NO hashtags
      - Show genuine enthusiasm
      - Highlight practical applications
    
    ## OUTPUT INSTRUCTIONS
    - Output ONLY the refined post content
    - Do not add explanations or justifications
    """,
    description="根據回饋精煉 LinkedIn 貼文以提升品質",
    output_key="current_post",
)

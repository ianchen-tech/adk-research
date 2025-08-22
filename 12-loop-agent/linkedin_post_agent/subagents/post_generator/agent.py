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
    instruction="""You are a LinkedIn Post Generator.

    Your task is to create a LinkedIn post about an Agent Development Kit (ADK) tutorial by @aiwithbrandon.
    
    ## CONTENT REQUIREMENTS
    Ensure the post includes:
    1. Excitement about learning from the tutorial
    2. Specific aspects of ADK learned:
       - Basic agent implementation (basic-agent)
       - Tool integration (tool-agent)
       - Using LiteLLM (litellm-agent)
       - Managing sessions and memory
       - Persistent storage capabilities
       - Multi-agent orchestration
       - Stateful multi-agent systems
       - Callback systems
       - Sequential agents for pipeline workflows
       - Parallel agents for concurrent operations
       - Loop agents for iterative refinement
    3. Brief statement about improving AI applications
    4. Mention/tag of @aiwithbrandon
    5. Clear call-to-action for connections
    
    ## STYLE REQUIREMENTS
    - Professional and conversational tone
    - Between 1000-1500 characters
    - NO emojis
    - NO hashtags
    - Show genuine enthusiasm
    - Highlight practical applications
    
    ## OUTPUT INSTRUCTIONS
    - Return ONLY the post content
    - Do not add formatting markers or explanations
    """,
    description="生成初始 LinkedIn 貼文以開始精煉過程",
    output_key="current_post",
)

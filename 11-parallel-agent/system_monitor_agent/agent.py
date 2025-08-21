"""系統監控根代理

此模組定義了系統監控應用程式的根代理。
它使用並行代理進行系統資訊收集，並使用順序
管道進行整體流程。
"""

from google.adk.agents import ParallelAgent, SequentialAgent

from .subagents.cpu_info_agent import cpu_info_agent
from .subagents.disk_info_agent import disk_info_agent
from .subagents.memory_info_agent import memory_info_agent
from .subagents.synthesizer_agent import system_report_synthesizer

# --- 1. 建立並行代理以同時收集資訊 ---
system_info_gatherer = ParallelAgent(
    name="system_info_gatherer",
    sub_agents=[cpu_info_agent, memory_info_agent, disk_info_agent],
)

# --- 2. 建立順序管道以並行收集資訊，然後進行合成 ---
root_agent = SequentialAgent(
    name="system_monitor_agent",
    sub_agents=[system_info_gatherer, system_report_synthesizer],
)

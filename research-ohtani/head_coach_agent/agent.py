"""

"""

from google.adk.agents import SequentialAgent, ParallelAgent, LoopAgent

from .subagents.cpu_info_agent import cpu_info_agent
from .subagents.disk_info_agent import disk_info_agent
from .subagents.memory_info_agent import memory_info_agent
from .subagents.synthesizer_agent import system_report_synthesizer

# --- 1. Create Parallel Agent to ... ---
system_info_gatherer = ParallelAgent(
    name="system_info_gatherer",
    sub_agents=[cpu_info_agent, memory_info_agent, disk_info_agent],
)

# --- 1. Create Parallel Agent to ... ---
system_info_gatherer = ParallelAgent(
    name="system_info_gatherer",
    sub_agents=[cpu_info_agent, memory_info_agent, disk_info_agent],
)

# --- 1. Create Parallel Agent to ... ---
system_info_gatherer = ParallelAgent(
    name="system_info_gatherer",
    sub_agents=[cpu_info_agent, memory_info_agent, disk_info_agent],
)

# --- 2. Create Sequential Agent to ... ---
root_agent = SequentialAgent(
    name="head_coach_agent",
    sub_agents=[system_info_gatherer, system_report_synthesizer],
)

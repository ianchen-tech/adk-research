#!/usr/bin/env python3
"""
測試重構後的 head_coach_agent 是否能正常載入和初始化
"""

try:
    from head_coach_agent.agent import head_coach_agent
    print("✅ head_coach_agent 匯入成功")
    
    # 測試代理屬性
    print(f"代理名稱: {head_coach_agent.name}")
    print(f"代理類型: {type(head_coach_agent).__name__}")
    print(f"子代理數量: {len(head_coach_agent.sub_agents)}")
    
    # 列出子代理
    for i, sub_agent in enumerate(head_coach_agent.sub_agents):
        print(f"子代理 {i+1}: {sub_agent.name} ({type(sub_agent).__name__})")
        if hasattr(sub_agent, 'sub_agents'):
            for j, sub_sub_agent in enumerate(sub_agent.sub_agents):
                print(f"  - 子代理 {j+1}: {sub_sub_agent.name} ({type(sub_sub_agent).__name__})")
    
    # 特別測試 data_coach_agent 是否正確匯入
    from head_coach_agent.subagents.data_coach_agent.agent import data_coach_agent
    print(f"\n✅ data_coach_agent 獨立匯入成功")
    print(f"data_coach_agent 名稱: {data_coach_agent.name}")
    print(f"data_coach_agent 類型: {type(data_coach_agent).__name__}")
    print(f"data_coach_agent 工具數量: {len(data_coach_agent.tools)}")
    
    print("\n✅ 所有測試通過！重構後的代理結構正常運作")
    
except ImportError as e:
    print(f"❌ 匯入錯誤: {e}")
except Exception as e:
    print(f"❌ 其他錯誤: {e}")
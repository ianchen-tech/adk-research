"""記憶體資訊工具

此模組提供收集記憶體資訊的工具。
"""

import time
from typing import Any, Dict

import psutil


def get_memory_info() -> Dict[str, Any]:
    """
    收集記憶體資訊，包括 RAM 和交換記憶體使用情況。

    Returns:
        Dict[str, Any]: 為 ADK 結構化的記憶體資訊字典
    """
    try:
        # 取得記憶體資訊
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        memory_info = {
            "total_memory": f"{memory.total / (1024 ** 3):.2f} GB",
            "available_memory": f"{memory.available / (1024 ** 3):.2f} GB",
            "used_memory": f"{memory.used / (1024 ** 3):.2f} GB",
            "memory_percentage": f"{memory.percent:.1f}%",
            "swap_total": f"{swap.total / (1024 ** 3):.2f} GB",
            "swap_used": f"{swap.used / (1024 ** 3):.2f} GB",
            "swap_percentage": f"{swap.percent:.1f}%",
        }

        # 計算統計資料
        memory_usage = memory.percent
        swap_usage = swap.percent
        high_memory_usage = memory_usage > 80
        high_swap_usage = swap_usage > 80

        # 格式化為 ADK 工具返回結構
        return {
            "result": memory_info,
            "stats": {
                "memory_usage_percentage": memory_usage,
                "swap_usage_percentage": swap_usage,
                "total_memory_gb": memory.total / (1024**3),
                "available_memory_gb": memory.available / (1024**3),
            },
            "additional_info": {
                "data_format": "dictionary",
                "collection_timestamp": time.time(),
                "performance_concern": (
                    "偵測到高記憶體使用率" if high_memory_usage else None
                ),
                "swap_concern": "偵測到高交換記憶體使用率" if high_swap_usage else None,
            },
        }
    except Exception as e:
        return {
            "result": {"error": f"無法收集記憶體資訊：{str(e)}"},
            "stats": {"success": False},
            "additional_info": {"error_type": str(type(e).__name__)},
        }

"""CPU 資訊工具

此模組提供收集 CPU 資訊的工具。
"""

import time
from typing import Any, Dict

import psutil


def get_cpu_info() -> Dict[str, Any]:
    """
    收集 CPU 資訊，包括核心數量和使用情況。

    Returns:
        Dict[str, Any]: 為 ADK 結構化的 CPU 資訊字典
    """
    try:
        # 取得 CPU 資訊
        cpu_info = {
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "cpu_usage_per_core": [
                f"Core {i}: {percentage:.1f}%"
                for i, percentage in enumerate(
                    psutil.cpu_percent(interval=1, percpu=True)
                )
            ],
            "avg_cpu_usage": f"{psutil.cpu_percent(interval=1):.1f}%",
        }

        # 計算結果摘要的一些統計資料
        avg_usage = float(cpu_info["avg_cpu_usage"].strip("%"))
        high_usage = avg_usage > 80

        # 格式化為 ADK 工具返回結構
        return {
            "result": cpu_info,
            "stats": {
                "physical_cores": cpu_info["physical_cores"],
                "logical_cores": cpu_info["logical_cores"],
                "avg_usage_percentage": avg_usage,
                "high_usage_alert": high_usage,
            },
            "additional_info": {
                "data_format": "dictionary",
                "collection_timestamp": time.time(),
                "performance_concern": (
                    "偵測到高 CPU 使用率" if high_usage else None
                ),
            },
        }
    except Exception as e:
        return {
            "result": {"error": f"無法收集 CPU 資訊：{str(e)}"},
            "stats": {"success": False},
            "additional_info": {"error_type": str(type(e).__name__)},
        }

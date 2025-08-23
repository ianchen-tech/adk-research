"""LinkedIn 貼文審查器代理工具

此模組提供分析和驗證 LinkedIn 貼文的工具。
"""

from typing import Any, Dict

from google.adk.tools.tool_context import ToolContext


def count_characters(text: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    計算提供文字中的字元數並提供基於長度的回饋工具。
    根據長度要求更新狀態中的 review_status。

    Args:
        text: 要分析字元數的文字
        tool_context: 用於存取和更新會話狀態的上下文

    Returns:
        Dict[str, Any]: 包含以下內容的字典：
            - result: 'fail' 或 'pass'
            - char_count: 文字中的字元數
            - message: 關於長度的回饋訊息
    """
    char_count = len(text)
    MIN_LENGTH = 1000
    MAX_LENGTH = 1500

    print("\n----------- 工具除錯 -----------")
    print(f"檢查文字長度：{char_count} 字元")
    print("----------------------------------\n")

    if char_count < MIN_LENGTH:
        chars_needed = MIN_LENGTH - char_count
        tool_context.state["review_status"] = "fail"
        return {
            "result": "fail",
            "char_count": char_count,
            "chars_needed": chars_needed,
            "message": f"貼文太短。需要增加 {chars_needed} 個字元以達到最小長度 {MIN_LENGTH}。",
        }
    elif char_count > MAX_LENGTH:
        chars_to_remove = char_count - MAX_LENGTH
        tool_context.state["review_status"] = "fail"
        return {
            "result": "fail",
            "char_count": char_count,
            "chars_to_remove": chars_to_remove,
            "message": f"貼文太長。需要移除 {chars_to_remove} 個字元以符合最大長度 {MAX_LENGTH}。",
        }
    else:
        tool_context.state["review_status"] = "pass"
        return {
            "result": "pass",
            "char_count": char_count,
            "message": f"貼文長度良好（{char_count} 字元）。",
        }


def exit_loop(tool_context: ToolContext) -> Dict[str, Any]:
    """
    僅當貼文滿足所有品質要求時才呼叫此函數，
    表示反覆過程應該結束。

    Args:
        tool_context: 工具執行的上下文

    Returns:
        空字典
    """
    print("\n----------- 退出循環已觸發 -----------")
    print("貼文審查成功完成")
    print("循環即將退出")
    print("------------------------------------------\n")

    tool_context.actions.escalate = True
    return {}

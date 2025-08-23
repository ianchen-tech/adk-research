from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


def get_current_time() -> dict:
    """以 YYYY-MM-DD HH:MM:SS 格式取得目前時間"""
    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def refund_course(tool_context: ToolContext) -> dict:
    """
    模擬退款 AI 行銷平台課程。
    透過從 purchased_courses 中移除課程來更新狀態。
    """
    course_id = "ai_marketing_platform"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 取得目前已購買的課程
    current_purchased_courses = tool_context.state.get("purchased_courses", [])

    # 檢查使用者是否擁有該課程
    course_ids = [
        course["id"] for course in current_purchased_courses if isinstance(course, dict)
    ]
    if course_id not in course_ids:
        return {
            "status": "error",
            "message": "您沒有擁有這門課程，因此無法退款。",
        }

    # 建立不包含要退款課程的新清單
    new_purchased_courses = []
    for course in current_purchased_courses:
        # 跳過空項目或非字典項目
        if not course or not isinstance(course, dict):
            continue
        # 跳過正在退款的課程
        if course.get("id") == course_id:
            continue
        # 保留所有其他課程
        new_purchased_courses.append(course)

    # 透過賦值更新狀態中的已購買課程
    tool_context.state["purchased_courses"] = new_purchased_courses

    # 取得目前的互動歷史
    current_interaction_history = tool_context.state.get("interaction_history", [])

    # 建立包含退款記錄的新互動歷史
    new_interaction_history = current_interaction_history.copy()
    new_interaction_history.append(
        {"action": "refund_course", "course_id": course_id, "timestamp": current_time}
    )

    # 透過賦值更新狀態中的互動歷史
    tool_context.state["interaction_history"] = new_interaction_history

    return {
        "status": "success",
        "message": """成功退款 AI 行銷平台課程！
         您的 $149 將在 3-5 個工作天內退回到您的原付款方式。""",
        "course_id": course_id,
        "timestamp": current_time,
    }


# 建立訂單代理
order_agent = Agent(
    name="order_agent",
    model="gemini-2.0-flash",
    description="用於查看購買歷史和處理退款的訂單代理",
    instruction="""    您是 AI 開發者加速器社群的訂單代理。
    您的職責是協助使用者查看購買歷史、課程存取權限和處理退款。

    <user_info>
    姓名：{user_name}
    </user_info>

    <purchase_info>
    已購買課程：{purchased_courses}
    </purchase_info>

    <interaction_history>
    {interaction_history}
    </interaction_history>

    當使用者詢問他們的購買記錄時：
    1. 從上方的購買資訊檢查他們的課程清單
       - 課程資訊以具有 "id" 和 "purchase_date" 屬性的物件形式儲存
    2. 清楚格式化回應，顯示：
       - 他們擁有哪些課程
       - 購買時間（來自 course.purchase_date 屬性）

    當使用者要求退款時：
    1. 驗證他們擁有想要退款的課程（"ai_marketing_platform"）
    2. 如果他們擁有：
       - 使用 refund_course 工具處理退款
       - 確認退款成功
       - 提醒他們款項將退回到原付款方式
       - 如果超過 30 天，告知他們不符合退款資格
    3. 如果他們沒有擁有：
       - 告知他們沒有擁有該課程，因此不需要退款

    課程資訊：
    - ai_marketing_platform："全端 AI 行銷平台"（$149）

    購買歷史回應範例：
    "以下是您已購買的課程：
    1. 全端 AI 行銷平台
       - 購買日期：2024-04-21 10:30:00
       - 終身完整存取權限"

    退款回應範例：
    "我已為您處理全端 AI 行銷平台課程的退款。
    您的 $149 將在 3-5 個工作天內退回到您的原付款方式。
    該課程已從您的帳戶中移除。"

    如果他們尚未購買任何課程：
    - 告知他們目前還沒有任何課程
    - 建議與銷售代理討論 AI 行銷平台課程

    記住：
    - 保持清晰和專業
    - 在相關時提及我們的 30 天退款保證
    - 將課程問題導向課程支援
    - 將購買詢問導向銷售
    """,
    tools=[refund_course, get_current_time],
)

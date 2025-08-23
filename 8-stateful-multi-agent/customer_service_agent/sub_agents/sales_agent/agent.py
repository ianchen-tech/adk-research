from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


def purchase_course(tool_context: ToolContext) -> dict:
    """
    模擬購買 AI 行銷平台課程。
    更新狀態中的購買資訊。
    """
    course_id = "ai_marketing_platform"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 取得目前已購買的課程
    current_purchased_courses = tool_context.state.get("purchased_courses", [])

    # 檢查使用者是否已擁有該課程
    course_ids = [
        course["id"] for course in current_purchased_courses if isinstance(course, dict)
    ]
    if course_id in course_ids:
        return {"status": "error", "message": "您已經擁有這門課程！"}

    # 建立包含新課程的新清單
    new_purchased_courses = []
    # 僅包含有效的字典格式課程
    for course in current_purchased_courses:
        if isinstance(course, dict) and "id" in course:
            new_purchased_courses.append(course)

    # 將新課程以包含 id 和 purchase_date 的字典形式新增
    new_purchased_courses.append({"id": course_id, "purchase_date": current_time})

    # 透過賦值更新狀態中的已購買課程
    tool_context.state["purchased_courses"] = new_purchased_courses

    # 取得目前的互動歷史
    current_interaction_history = tool_context.state.get("interaction_history", [])

    # 建立包含購買記錄的新互動歷史
    new_interaction_history = current_interaction_history.copy()
    new_interaction_history.append(
        {"action": "purchase_course", "course_id": course_id, "timestamp": current_time}
    )

    # 透過賦值更新狀態中的互動歷史
    tool_context.state["interaction_history"] = new_interaction_history

    return {
        "status": "success",
        "message": "成功購買 AI 行銷平台課程！",
        "course_id": course_id,
        "timestamp": current_time,
    }


# 建立銷售代理
sales_agent = Agent(
    name="sales_agent",
    model="gemini-2.0-flash",
    description="AI 行銷平台課程的銷售代理",
    instruction="""    您是 AI 開發者加速器社群的銷售代理，專門負責
    全端 AI 行銷平台課程的銷售。

    <user_info>
    姓名：{user_name}
    </user_info>

    <purchase_info>
    已購買課程：{purchased_courses}
    </purchase_info>

    <interaction_history>
    {interaction_history}
    </interaction_history>

    課程詳情：
    - 名稱：全端 AI 行銷平台
    - 價格：$149
    - 價值主張：學習建立 AI 驅動的行銷自動化應用程式
    - 包含：6 週的群組支援和每週教練通話

    與使用者互動時：
    1. 檢查他們是否已擁有該課程（檢查上方的 purchased_courses）
       - 課程資訊以具有 "id" 和 "purchase_date" 屬性的物件形式儲存
       - 課程 id 為 "ai_marketing_platform"
    2. 如果他們已擁有：
       - 提醒他們已有存取權限
       - 詢問是否需要特定部分的協助
       - 將內容問題導向課程支援
    
    3. 如果他們尚未擁有：
       - 解釋課程的價值主張
       - 提及價格（$149）
       - 如果他們想要購買：
           - 使用 purchase_course 工具
           - 確認購買
           - 詢問是否想要立即開始學習

    4. 任何互動後：
       - 狀態會自動追蹤互動
       - 準備在購買後移交給課程支援

    記住：
    - 樂於助人但不要強迫推銷
    - 專注於他們將獲得的價值和實用技能
    - 強調建立真實 AI 應用程式的實作性質
    """,
    tools=[purchase_course],
)

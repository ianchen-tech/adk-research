from datetime import datetime

from google.genai import types


# 終端輸出的 ANSI 顏色代碼
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    # 前景顏色
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # 背景顏色
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


def update_interaction_history(session_service, app_name, user_id, session_id, entry):
    """在狀態中新增一個條目到互動歷史。

    Args:
        session_service: 會話服務實例
        app_name: 應用程式名稱
        user_id: 使用者 ID
        session_id: 會話 ID
        entry: 包含互動資料的字典
            - 需要 'action' 鍵（例如：'user_query'、'agent_response'）
            - 其他鍵根據動作類型而靈活變化
    """
    try:
        # 取得目前會話
        session = session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )

        # 取得目前互動歷史
        interaction_history = session.state.get("interaction_history", [])

        # 如果尚未存在則新增時間戳記
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 將條目新增到互動歷史
        interaction_history.append(entry)

        # 建立更新的狀態
        updated_state = session.state.copy()
        updated_state["interaction_history"] = interaction_history

        # 使用更新的狀態建立新會話
        session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            state=updated_state,
        )
    except Exception as e:
        print(f"更新互動歷史時發生錯誤：{e}")


def add_user_query_to_history(session_service, app_name, user_id, session_id, query):
    """將使用者查詢新增到互動歷史。"""
    update_interaction_history(
        session_service,
        app_name,
        user_id,
        session_id,
        {
            "action": "user_query",
            "query": query,
        },
    )


def add_agent_response_to_history(
    session_service, app_name, user_id, session_id, agent_name, response
):
    """將代理回應新增到互動歷史。"""
    update_interaction_history(
        session_service,
        app_name,
        user_id,
        session_id,
        {
            "action": "agent_response",
            "agent": agent_name,
            "response": response,
        },
    )


def display_state(
    session_service, app_name, user_id, session_id, label="目前狀態"
):
    """以格式化方式顯示目前會話狀態。"""
    try:
        session = session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )

        # 使用清晰的區段格式化輸出
        print(f"\n{'-' * 10} {label} {'-' * 10}")

        # 處理使用者名稱
        user_name = session.state.get("user_name", "未知")
        print(f"👤 使用者：{user_name}")

        # 處理已購買課程
        purchased_courses = session.state.get("purchased_courses", [])
        if purchased_courses and any(purchased_courses):
            print("📚 課程：")
            for course in purchased_courses:
                if isinstance(course, dict):
                    course_id = course.get("id", "未知")
                    purchase_date = course.get("purchase_date", "未知日期")
                    print(f"  - {course_id}（購買於 {purchase_date}）")
                elif course:  # 處理字串格式以保持向後相容性
                    print(f"  - {course}")
        else:
            print("📚 課程：無")

        # 以更易讀的方式處理互動歷史
        interaction_history = session.state.get("interaction_history", [])
        if interaction_history:
            print("📝 互動歷史：")
            for idx, interaction in enumerate(interaction_history, 1):
                # 美化格式化字典條目，或僅顯示字串
                if isinstance(interaction, dict):
                    action = interaction.get("action", "interaction")
                    timestamp = interaction.get("timestamp", "未知時間")

                    if action == "user_query":
                        query = interaction.get("query", "")
                        print(f'  {idx}. 使用者查詢於 {timestamp}："{query}"')
                    elif action == "agent_response":
                        agent = interaction.get("agent", "未知")
                        response = interaction.get("response", "")
                        # 截斷過長的回應以便顯示
                        if len(response) > 100:
                            response = response[:97] + "..."
                        print(f'  {idx}. {agent} 回應於 {timestamp}："{response}"')
                    else:
                        details = ", ".join(
                            f"{k}: {v}"
                            for k, v in interaction.items()
                            if k not in ["action", "timestamp"]
                        )
                        print(
                            f"  {idx}. {action} at {timestamp}"
                            + (f" ({details})" if details else "")
                        )
                else:
                    print(f"  {idx}. {interaction}")
        else:
            print("📝 互動歷史：無")

        # 顯示可能存在的任何其他狀態鍵
        other_keys = [
            k
            for k in session.state.keys()
            if k not in ["user_name", "purchased_courses", "interaction_history"]
        ]
        if other_keys:
            print("🔑 其他狀態：")
            for key in other_keys:
                print(f"  {key}: {session.state[key]}")

        print("-" * (22 + len(label)))
    except Exception as e:
        print(f"顯示狀態時發生錯誤：{e}")


async def process_agent_response(event):
    """處理並顯示代理回應事件。"""
    print(f"事件 ID：{event.id}，作者：{event.author}")

    # 首先檢查特定部分
    has_specific_part = False
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "text") and part.text and not part.text.isspace():
                print(f"  文字：'{part.text.strip()}'")

    # 在特定部分後檢查最終回應
    final_response = None
    if not has_specific_part and event.is_final_response():
        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text")
            and event.content.parts[0].text
        ):
            final_response = event.content.parts[0].text.strip()
            # 使用顏色和格式化讓最終回應更突出
            print(
                f"\n{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╔══ 代理回應 ═════════════════════════════════════════{Colors.RESET}"
            )
            print(f"{Colors.CYAN}{Colors.BOLD}{final_response}{Colors.RESET}")
            print(
                f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╚═════════════════════════════════════════════════════════════{Colors.RESET}\n"
            )
        else:
            print(
                f"\n{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD}==> 最終代理回應：[最終事件中無文字內容]{Colors.RESET}\n"
            )

    return final_response


async def call_agent_async(runner, user_id, session_id, query):
    """使用使用者的查詢非同步呼叫代理。"""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(
        f"\n{Colors.BG_GREEN}{Colors.BLACK}{Colors.BOLD}--- 執行查詢：{query} ---{Colors.RESET}"
    )
    final_response_text = None
    agent_name = None

    # 在處理訊息前顯示狀態
    display_state(
        runner.session_service,
        runner.app_name,
        user_id,
        session_id,
        "處理前狀態",
    )

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            # 如果可用，從事件中擷取代理名稱
            if event.author:
                agent_name = event.author

            response = await process_agent_response(event)
            if response:
                final_response_text = response
    except Exception as e:
        print(f"{Colors.BG_RED}{Colors.WHITE}代理執行期間發生錯誤：{e}{Colors.RESET}")

    # 如果我們得到最終回應，將代理回應新增到互動歷史
    if final_response_text and agent_name:
        add_agent_response_to_history(
            runner.session_service,
            runner.app_name,
            user_id,
            session_id,
            agent_name,
            final_response_text,
        )

    # 在處理訊息後顯示狀態
    display_state(
        runner.session_service,
        runner.app_name,
        user_id,
        session_id,
        "處理後狀態",
    )

    print(f"{Colors.YELLOW}{'-' * 30}{Colors.RESET}")
    return final_response_text

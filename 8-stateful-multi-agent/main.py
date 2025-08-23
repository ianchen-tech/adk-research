import asyncio

# 匯入主要的客戶服務代理
from customer_service_agent.agent import customer_service_agent
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils import add_user_query_to_history, call_agent_async

load_dotenv()

# ===== 第一部分：初始化記憶體內會話服務 =====
# 此範例使用記憶體內儲存（非持久性）
session_service = InMemorySessionService()


# ===== 第二部分：定義初始狀態 =====
# 這將在建立新會話時使用
initial_state = {
    "user_name": "Brandon Hancock",
    "purchased_courses": [],
    "interaction_history": [],
}


async def main_async():
    # 設定常數
    APP_NAME = "客戶支援"
    USER_ID = "aiwithbrandon"

    # ===== 第三部分：會話建立 =====
    # 使用初始狀態建立新會話
    new_session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )
    SESSION_ID = new_session.id
    print(f"已建立新會話：{SESSION_ID}")

    # ===== 第四部分：代理執行器設定 =====
    # 使用主要客戶服務代理建立執行器
    runner = Runner(
        agent=customer_service_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # ===== 第五部分：互動對話迴圈 =====
    print("\n歡迎使用客戶服務聊天！")
    print("輸入 'exit' 或 'quit' 結束對話。\n")

    while True:
        # 取得使用者輸入
        user_input = input("您：")

        # 檢查使用者是否想要退出
        if user_input.lower() in ["exit", "quit"]:
            print("結束對話。再見！")
            break

        # 使用使用者的查詢更新互動歷史
        add_user_query_to_history(
            session_service, APP_NAME, USER_ID, SESSION_ID, user_input
        )

        # 透過代理處理使用者查詢
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

    # ===== 第六部分：狀態檢查 =====
    # 顯示最終會話狀態
    final_session = session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    print("\n最終會話狀態：")
    for key, value in final_session.state.items():
        print(f"{key}: {value}")


def main():
    """應用程式的進入點。"""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()

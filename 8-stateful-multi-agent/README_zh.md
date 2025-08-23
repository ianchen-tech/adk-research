# ADK 中的狀態化多代理系統

此範例展示如何在 ADK 中創建狀態化多代理系統，結合持久狀態管理與專業代理委派的強大功能。這種方法創建了智能代理系統，能夠在互動過程中記住用戶資訊，同時利用專業領域的專業知識。

## 什麼是狀態化多代理系統？

狀態化多代理系統結合了兩種強大的模式：

1. **狀態管理**：在互動過程中持久化用戶和對話資訊
2. **多代理架構**：根據專業知識在專業代理之間分配任務

結果是一個複雜的代理生態系統，能夠：
- 記住用戶資訊和互動歷史
- 將查詢路由到最合適的專業代理
- 基於過去的互動提供個人化回應
- 在多個代理委派之間維持上下文

此範例實現了一個線上課程平台的客戶服務系統，其中專業代理處理客戶支援的不同方面，同時共享共同狀態。

## 專案結構

```
7-stateful-multi-agent/
│
├── customer_service_agent/         # 主要代理套件
│   ├── __init__.py                 # ADK 發現所需
│   ├── agent.py                    # 根代理定義
│   └── sub_agents/                 # 專業代理
│       ├── course_support_agent/   # 處理課程內容問題
│       ├── order_agent/            # 管理訂單歷史和退款
│       ├── policy_agent/           # 回答政策問題
│       └── sales_agent/            # 處理課程購買
│
├── main.py                         # 應用程式進入點與會話設定
├── utils.py                        # 狀態管理的輔助函數
├── .env                            # 環境變數
└── README.md                       # 此文件
```

## 關鍵組件

### 1. 會話管理

此範例使用 `InMemorySessionService` 來儲存會話狀態：

```python
session_service = InMemorySessionService()

def initialize_state():
    """使用預設值初始化會話狀態。"""
    return {
        "user_name": "Brandon Hancock",
        "purchased_courses": [""],
        "interaction_history": [],
    }

# 使用初始狀態創建新會話
session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initialize_state(),
)
```

### 2. 代理間的狀態共享

系統中的所有代理都可以存取相同的會話狀態，實現：
- 根代理追蹤互動歷史
- 銷售代理更新已購買課程
- 課程支援代理檢查用戶是否已購買特定課程
- 所有代理基於用戶資訊個人化回應

### 3. 多代理委派

客戶服務代理將查詢路由到專業子代理：

```python
customer_service_agent = Agent(
    name="customer_service",
    model="gemini-2.0-flash",
    description="AI Developer Accelerator 社群的客戶服務代理",
    instruction="""
    您是 AI Developer Accelerator 社群的主要客戶服務代理。
    您的角色是幫助用戶解決問題，並將他們導向適當的專業代理。
    
    # ... 詳細指示 ...
    
    """,
    sub_agents=[policy_agent, sales_agent, course_support_agent, order_agent],
    tools=[get_current_time],
)
```

## 運作方式

1. **初始會話創建**：
   - 使用用戶資訊和空的互動歷史創建新會話
   - 會話狀態使用預設值初始化

2. **對話追蹤**：
   - 每個用戶訊息都會添加到狀態中的 `interaction_history`
   - 代理可以查看過去的互動以維持上下文

3. **查詢路由**：
   - 根代理分析用戶查詢並決定哪個專家應該處理
   - 專業代理在被委派時會收到完整的狀態上下文

4. **狀態更新**：
   - 當用戶購買課程時，銷售代理會更新 `purchased_courses`
   - 這些更新對所有代理在未來的互動中都可用

5. **個人化回應**：
   - 代理根據購買歷史和先前互動調整回應
   - 根據用戶已購買的內容採取不同路徑

## 開始使用

### 設定

1. 從根目錄啟動虛擬環境：
```bash
# macOS/Linux:
source ../.venv/bin/activate
# Windows CMD:
..\venv\Scripts\activate.bat
# Windows PowerShell:
..\venv\Scripts\Activate.ps1
```

2. 確保您的 Google API 金鑰已在 `.env` 檔案中設定：
```
GOOGLE_API_KEY=your_api_key_here
```

### 執行範例

要執行狀態化多代理範例：

```bash
python main.py
```

這將：
1. 使用預設狀態初始化新會話
2. 開始與客戶服務代理的互動對話
3. 在會話狀態中追蹤所有互動
4. 允許專業代理處理特定查詢

### 範例對話流程

嘗試此對話流程來測試系統：

1. **從一般查詢開始**：
   - "你們提供什麼課程？"
   - （根代理將路由到銷售代理）

2. **詢問購買**：
   - "我想購買 AI 行銷平台課程"
   - （銷售代理將處理購買並更新狀態）

3. **詢問課程內容**：
   - "你能告訴我 AI 行銷平台課程的內容嗎？"
   - （根代理將路由到課程支援代理，現在有存取權限）

4. **詢問退款**：
   - "你們的退款政策是什麼？"
   - （根代理將路由到政策代理）

注意系統如何在不同的專業代理之間記住您的購買！

## 進階功能

### 1. 互動歷史追蹤

系統維護互動歷史以提供上下文：

```python
# 使用用戶查詢更新互動歷史
add_user_query_to_history(
    session_service, APP_NAME, USER_ID, SESSION_ID, user_input
)
```

### 2. 動態存取控制

系統實現對某些代理的條件存取：

```
3. 課程支援代理
   - 用於課程內容問題
   - 僅對用戶已購買的課程可用
   - 在導向此處之前檢查 "ai_marketing_platform" 是否在已購買課程中
```

### 3. 基於狀態的個人化

所有代理根據會話狀態調整回應：

```
根據用戶的購買歷史和先前互動調整您的回應。
當用戶尚未購買任何課程時，鼓勵他們探索 AI 行銷平台。
當用戶已購買課程時，為這些特定課程提供支援。
```

## 生產考量

對於生產實現，請考慮：

1. **持久儲存**：將 `InMemorySessionService` 替換為 `DatabaseSessionService` 以在應用程式重啟時持久化狀態
2. **用戶認證**：實現適當的用戶認證以安全地識別用戶
3. **錯誤處理**：為代理失敗和狀態損壞添加強健的錯誤處理
4. **監控**：實現日誌記錄和監控以追蹤系統效能

## 其他資源

- [ADK 會話文件](https://google.github.io/adk-docs/sessions/session/)
- [ADK 多代理系統文件](https://google.github.io/adk-docs/agents/multi-agent-systems/)
- [ADK 中的狀態管理](https://google.github.io/adk-docs/sessions/state/)
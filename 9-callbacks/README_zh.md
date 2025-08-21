# ADK 中的回調函數

此範例展示如何在代理開發工具包（ADK）中使用回調函數來攔截和修改代理在不同執行階段的行為。回調函數提供了強大的代理生命週期鉤子，讓您能夠添加自定義邏輯來進行監控、日誌記錄、內容過濾和結果轉換。

## 什麼是 ADK 中的回調函數？

回調函數是在代理執行流程中特定時點執行的函數。它們允許您：

1. **監控和日誌記錄**：追蹤代理活動和性能指標
2. **過濾內容**：阻止不當的請求或回應
3. **轉換數據**：修改代理工作流程中的輸入和輸出
4. **實施安全政策**：強制執行合規性和安全措施
5. **添加自定義邏輯**：在代理流程中插入業務特定的處理

ADK 提供了幾種類型的回調函數，可以附加到代理系統的不同組件上。

## 回調參數和上下文

每種類型的回調函數都提供對特定上下文物件的訪問，這些物件包含有關當前執行狀態的寶貴資訊。理解這些參數是構建有效回調函數的關鍵。

### CallbackContext

`CallbackContext` 物件提供給所有回調類型，包含：

- **`agent_name`**：正在執行的代理名稱
- **`invocation_id`**：當前代理調用的唯一識別符
- **`state`**：訪問會話狀態，允許您讀取/寫入持久數據
- **`app_name`**：應用程式名稱
- **`user_id`**：當前用戶的 ID
- **`session_id`**：當前會話的 ID

使用範例：
```python
def my_callback(callback_context: CallbackContext, ...):
    # 訪問狀態來儲存或檢索數據
    user_name = callback_context.state.get("user_name", "Unknown")
    
    # 記錄當前代理和調用
    print(f"Agent {callback_context.agent_name} executing (ID: {callback_context.invocation_id})")
```

### ToolContext（用於工具回調）

`ToolContext` 物件提供給工具回調，包含：

- **`agent_name`**：發起工具調用的代理名稱
- **`state`**：訪問會話狀態，允許工具讀取/修改共享數據
- **`properties`**：工具執行特定的額外屬性

使用範例：
```python
def before_tool_callback(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext):
    # 在狀態中記錄工具使用情況
    tools_used = tool_context.state.get("tools_used", [])
    tools_used.append(tool.name)
    tool_context.state["tools_used"] = tools_used
```

### LlmRequest（用於模型回調）

`LlmRequest` 物件提供給 before_model_callback，包含：

- **`contents`**：表示對話歷史的 Content 物件列表
- **`generation_config`**：模型生成的配置
- **`safety_settings`**：模型的安全設定
- **`tools`**：提供給模型的工具

使用範例：
```python
def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest):
    # 獲取最後一條用戶訊息進行分析
    last_message = None
    for content in reversed(llm_request.contents):
        if content.role == "user" and content.parts:
            last_message = content.parts[0].text
            break
            
    # 分析用戶的訊息
    if last_message and contains_sensitive_info(last_message):
        # 返回一個繞過模型調用的回應
        return LlmResponse(...)
```

### LlmResponse（用於模型回調）

`LlmResponse` 物件從模型返回並提供給 after_model_callback：

- **`content`**：包含模型回應的 Content 物件
- **`tool_calls`**：模型想要進行的任何工具調用
- **`usage_metadata`**：關於模型使用的元數據（令牌等）

使用範例：
```python
def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse):
    # 訪問模型的文本回應
    if llm_response.content and llm_response.content.parts:
        response_text = llm_response.content.parts[0].text
        
        # 修改回應
        modified_text = transform_text(response_text)
        llm_response.content.parts[0].text = modified_text
        
        return llm_response
```

## 展示的回調類型

此專案包含三個回調模式的範例：

### 1. 代理回調（`before_after_agent/`）
- **代理前回調**：在代理處理開始時運行
- **代理後回調**：在代理完成處理後運行

### 2. 模型回調（`before_after_model/`）
- **模型前回調**：在請求到達 LLM 之前攔截請求
- **模型後回調**：在回應從 LLM 返回後修改回應

### 3. 工具回調（`before_after_tool/`）
- **工具前回調**：修改工具參數或跳過工具執行
- **工具後回調**：用額外資訊增強工具回應

## 專案結構
```
8-callbacks/
│
├── before_after_agent/           # 代理回調範例
│   ├── init .py               # ADK 發現所需
│   ├── agent.py                  # 帶有代理回調的代理
│   └── .env                      # 環境變數
│
├── before_after_model/           # 模型回調範例
│   ├── init .py               # ADK 發現所需
│   ├── agent.py                  # 帶有模型回調的代理
│   └── .env                      # 環境變數
│
├── before_after_tool/            # 工具回調範例
│   ├── init .py               # ADK 發現所需
│   ├── agent.py                  # 帶有工具回調的代理
│   └── .env                      # 環境變數
│
└── README.md                     # 此文檔
```


## 範例 1：代理回調

代理回調範例展示：

1. **請求日誌記錄**：記錄請求開始和結束的時間
2. **性能監控**：測量請求持續時間
3. **狀態管理**：使用會話狀態追蹤請求計數

### 關鍵實作細節

```python
def before_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    # 獲取會話狀態
    state = callback_context.state
    
    # 初始化請求計數器
    if "request_counter" not in state:
        state["request_counter"] = 1
    else:
        state["request_counter"] += 1
        
    # 儲存開始時間以計算持續時間
    state["request_start_time"] = datetime.now()
    
    # 記錄請求
    logger.info("=== AGENT EXECUTION STARTED ===")
    
    return None  # 繼續正常的代理處理

def after_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    # 獲取會話狀態
    state = callback_context.state
    
    # 計算請求持續時間
    duration = None
    if "request_start_time" in state:
        duration = (datetime.now() - state["request_start_time"]).total_seconds()
        
    # 記錄完成
    logger.info("=== AGENT EXECUTION COMPLETED ===")
    
    return None  # 繼續正常的代理處理
```

### 測試代理回調

任何互動都會展示代理回調，它們會記錄請求並測量持續時間。

## 範例 2：模型回調

模型回調範例展示：

1. **內容過濾**：在不當內容到達模型之前阻止它們
2. **回應轉換**：將負面詞彙替換為更積極的替代詞

### 關鍵實作細節

```python
def before_model_callback(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    # 檢查不當內容
    if last_user_message and "sucks" in last_user_message.lower():
        # 返回一個回應以跳過模型調用
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[
                    types.Part(
                        text="我無法回應包含不當語言的訊息..."
                    )
                ],
            )
        )
    # 返回 None 以繼續正常的模型請求
    return None

def after_model_callback(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    # 簡單的詞彙替換
    replacements = {
        "problem": "challenge",
        "difficult": "complex",
    }
    # 執行替換並返回修改後的回應
```

### 測試模型回調

測試 before_model_callback 中的內容過濾：
- "This website sucks, can you help me fix it?"
- "Everything about this project sucks."

測試 after_model_callback 中的詞彙替換：
- "What's the biggest problem with machine learning today?"
- "Why is debugging so difficult in complex systems?"
- "I have a problem with my code that's very difficult to solve."

## 範例 3：工具回調

工具回調範例展示：

1. **參數修改**：在工具執行前轉換輸入參數
2. **請求阻止**：完全阻止某些工具調用
3. **回應增強**：為工具回應添加額外上下文
4. **錯誤處理**：改善錯誤訊息以提供更好的用戶體驗

### 關鍵實作細節

```python
def before_tool_callback(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict]:
    # 修改參數（例如，將 "USA" 轉換為 "United States"）
    if args.get("country", "").lower() == "merica":
        args["country"] = "United States"
        return None
        
    # 對受限制的國家完全跳過調用
    if args.get("country", "").lower() == "restricted":
        return {"result": "對此資訊的訪問已被限制。"}
    
    return None  # 繼續正常的工具調用

def after_tool_callback(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:
    # 為任何美國首都回應添加註記
    if "washington" in tool_response.get("result", "").lower():
        modified_response = copy.deepcopy(tool_response)
        modified_response["result"] = f"{tool_response['result']} (註記：這是美國的首都。🇺🇸)"
        return modified_response
        
    return None  # 使用原始回應
```

### 測試工具回調

測試參數修改：
- "What is the capital of USA?"（轉換為 "United States"）
- "What is the capital of Merica?"（轉換為 "United States"）

測試請求阻止：
- "What is the capital of restricted?"（阻止請求）

測試回應增強：
- "What is the capital of the United States?"（添加愛國註記）

查看正常操作：
- "What is the capital of France?"（無修改）

## 運行範例

### 設定

1. 從根目錄啟動虛擬環境：
```bash
# macOS/Linux:
source ../.venv/bin/activate
# Windows CMD:
..\.venv\Scripts\activate.bat
# Windows PowerShell:
..\.venv\Scripts\Activate.ps1
```

2. 在每個代理目錄（`before_after_agent/`、`before_after_model/` 和 `before_after_tool/`）中基於提供的 `.env.example` 檔案創建 `.env` 檔案：
```
GOOGLE_API_KEY=your_api_key_here
```


### 運行範例

```bash
cd 8-callbacks
adk web
```

然後從網頁 UI 的下拉選單中選擇您想要測試的代理：
- "before_after_agent" 測試代理回調
- "before_after_model" 測試模型回調
- "before_after_tool" 測試工具回調

## 額外資源

- [ADK 回調文檔](https://google.github.io/adk-docs/callbacks/)
- [回調類型](https://google.github.io/adk-docs/callbacks/types-of-callbacks/)
- [設計模式和最佳實踐](https://google.github.io/adk-docs/callbacks/design-patterns-and-best-practices/)
# ADK 中的多代理系統

此範例展示如何在代理開發套件 (ADK) 中建立多代理系統，讓專業化的代理協作處理複雜任務，每個代理專注於其專業領域。

## 什麼是多代理系統？

多代理系統是代理開發套件 (ADK) 中的進階模式，允許多個專業化代理協作處理複雜任務。每個代理可以專注於特定領域或功能，並透過委派和溝通協作解決單一代理難以處理的問題。

## 專案結構需求

為了讓多代理系統在 ADK 中正常運作，您的專案必須遵循特定結構：

```
parent_folder/
├── root_agent_folder/           # 主代理套件 (例如 "manager")
│   ├── __init__.py              # 必須匯入 agent.py
│   ├── agent.py                 # 必須定義 root_agent
│   ├── .env                     # 環境變數
│   └── sub_agents/              # 所有子代理的目錄
│       ├── __init__.py          # 空白或匯入子代理
│       ├── agent_1_folder/      # 子代理套件
│       │   ├── __init__.py      # 必須匯入 agent.py
│       │   └── agent.py         # 必須定義 agent 變數
│       ├── agent_2_folder/
│       │   ├── __init__.py
│       │   └── agent.py
│       └── ...
```

### 必要結構組件：

1. **根代理套件**
   - 必須具有標準代理結構（如基本代理範例）
   - `agent.py` 檔案必須定義 `root_agent` 變數

2. **子代理目錄**
   - 通常組織為根代理資料夾內名為 `sub_agents` 的目錄
   - 每個子代理應在其自己的目錄中，遵循與一般代理相同的結構

3. **匯入子代理**
   - 根代理必須匯入子代理才能使用它們：
   ```python
   from .sub_agents.funny_nerd.agent import funny_nerd
   from .sub_agents.stock_analyst.agent import stock_analyst
   ```

4. **命令位置**
   - 始終從父目錄（`6-multi-agent`）執行 `adk web`，而不是從任何代理目錄內部

此結構確保 ADK 能夠發現並正確載入階層中的所有代理。

## 多代理架構選項

ADK 提供兩種主要方法來建構多代理系統：

### 1. 子代理委派模型

使用 `sub_agents` 參數，根代理可以完全委派任務給專業代理：

```python
root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="Manager agent",
    instruction="You are a manager agent that delegates tasks to specialized agents...",
    sub_agents=[stock_analyst, funny_nerd],
)
```

**特徵：**
- 完全委派 - 子代理接管整個回應
- 子代理的決定是最終的並控制對話
- 根代理充當「路由器」，決定哪個專家應該處理查詢

### 2. 代理作為工具模型

使用 `AgentTool` 包裝器，代理可以被其他代理用作工具：

```python
from google.adk.tools.agent_tool import AgentTool

root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="Manager agent",
    instruction="You are a manager agent that uses specialized agents as tools...",
    tools=[
        AgentTool(news_analyst),
        get_current_time,
    ],
)
```

**特徵：**
- 子代理將結果返回給根代理
- 根代理保持控制權，可以將子代理的回應納入自己的回應中
- 在單一回應中可以對不同的代理工具進行多次工具呼叫
- 給予根代理更多彈性來使用結果

## 使用多代理時的限制

### 子代理限制

**內建工具無法在子代理中使用。**

例如，在子代理中使用內建工具的這種方法目前**不**受支援：

```python
search_agent = Agent(
    model='gemini-2.0-flash',
    name='SearchAgent',
    instruction="You're a specialist in Google Search",
    tools=[google_search],  # 內建工具
)
coding_agent = Agent(
    model='gemini-2.0-flash',
    name='CodeAgent',
    instruction="You're a specialist in Code Execution",
    tools=[built_in_code_execution],  # 內建工具
)
root_agent = Agent(
    name="RootAgent",
    model="gemini-2.0-flash",
    description="Root Agent",
    sub_agents=[
        search_agent,  # 不支援
        coding_agent   # 不支援
    ],
)
```

### 使用代理工具的解決方法

要使用多個內建工具或將內建工具與其他工具結合，您可以使用 `AgentTool` 方法：

```python
from google.adk.tools import agent_tool

search_agent = Agent(
    model='gemini-2.0-flash',
    name='SearchAgent',
    instruction="You're a specialist in Google Search",
    tools=[google_search],
)
coding_agent = Agent(
    model='gemini-2.0-flash',
    name='CodeAgent',
    instruction="You're a specialist in Code Execution",
    tools=[built_in_code_execution],
)
root_agent = Agent(
    name="RootAgent",
    model="gemini-2.0-flash",
    description="Root Agent",
    tools=[
        agent_tool.AgentTool(agent=search_agent), 
        agent_tool.AgentTool(agent=coding_agent)
    ],
)
```

此方法將代理包裝為工具，允許根代理委派給各自使用單一內建工具的專業代理。

## 我們的多代理範例

此範例實作了一個與三個專業代理協作的管理代理：

1. **股票分析師**（子代理）：提供財務資訊和股市洞察
2. **有趣書呆子**（子代理）：創造關於技術主題的書呆子笑話
3. **新聞分析師**（代理工具）：提供當前科技新聞摘要

管理代理根據使用者請求的內容將查詢路由到適當的專家。

## 開始使用

此範例使用在根目錄中建立的相同虛擬環境。確保您已：

1. 從根目錄啟動虛擬環境：
```bash
# macOS/Linux:
source ../.venv/bin/activate
# Windows CMD:
..\.venv\Scripts\activate.bat
# Windows PowerShell:
..\.venv\Scripts\Activate.ps1
```

2. 設定您的 API 金鑰：
   - 將 manager 資料夾中的 `.env.example` 重新命名為 `.env`
   - 在 `.env` 檔案中將您的 Google API 金鑰新增到 `GOOGLE_API_KEY` 變數

## 執行範例

要執行多代理範例：

1. 導航到包含代理資料夾的 6-multi-agent 目錄。

2. 啟動互動式網頁 UI：
```bash
adk web
```

3. 在終端機中開啟顯示的 URL 來存取網頁 UI（通常是 http://localhost:8000）

4. 從 UI 左上角的下拉選單中選擇「manager」代理

5. 在螢幕底部的文字框中開始與您的代理聊天

### 疑難排解

如果您的多代理設定未正確出現在下拉選單中：
- 確保您從父目錄（6-multi-agent）執行 `adk web`
- 驗證每個代理的 `__init__.py` 正確匯入其各自的 `agent.py`
- 檢查根代理是否正確匯入所有子代理

### 可嘗試的範例提示

- "Can you tell me about the stock market today?"
- "Tell me something funny about programming"
- "What's the latest tech news?"
- "What time is it right now?"

您可以在終端機中按 `Ctrl+C` 來退出對話或停止伺服器。

## 其他資源

- [ADK 多代理系統文件](https://google.github.io/adk-docs/agents/multi-agent-systems/)
- [代理工具文件](https://google.github.io/adk-docs/tools/function-tools/#3-agent-as-a-tool)
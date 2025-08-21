# ADK 中的並行代理

此範例展示如何在代理開發套件 (ADK) 中實作並行代理。此範例中的主代理 `system_monitor_agent` 使用並行代理同時收集系統資訊，然後將其綜合成全面的系統健康報告。

## 什麼是並行代理？

並行代理是 ADK 中的工作流程代理，具有以下特點：

1. **並發執行**：子代理同時執行而非依序執行
2. **獨立運作**：每個子代理在執行期間獨立工作，不共享狀態
3. **提升效能**：大幅加速可並行執行任務的工作流程

當您需要高效執行多個獨立任務且時間是關鍵因素時，請使用並行代理。

## 系統監控範例

在此範例中，我們建立了一個使用並行代理收集系統資訊的系統監控應用程式。工作流程包括：

1. **並行系統資訊收集**：使用 `ParallelAgent` 同時收集以下資料：
   - CPU 使用率和統計資料
   - 記憶體使用率
   - 磁碟空間和使用情況

2. **順序報告綜合**：並行資料收集後，綜合代理將所有資訊結合成全面報告

### 子代理

1. **CPU 資訊代理**：收集和分析 CPU 資訊
   - 檢索核心數量、使用統計和效能指標
   - 識別潛在效能問題（高 CPU 使用率）

2. **記憶體資訊代理**：收集記憶體使用資訊
   - 收集總計、已使用和可用記憶體
   - 分析記憶體壓力和交換使用情況

3. **磁碟資訊代理**：分析磁碟空間和使用情況
   - 報告總計、已使用和可用磁碟空間
   - 識別空間不足的磁碟

4. **系統報告綜合器**：將所有收集的資訊結合成全面的系統健康報告
   - 建立系統健康的執行摘要
   - 將組件特定資訊組織成章節
   - 基於系統指標提供建議

### 運作方式

架構結合了並行和順序工作流程模式：

1. 首先，`system_info_gatherer` 並行代理同時執行所有三個資訊代理
2. 然後，`system_report_synthesizer` 使用收集的資料生成最終報告

這種混合方法展示了如何結合工作流程代理類型以獲得最佳效能和邏輯流程。

## 專案結構

```
10-parallel-agent/
│
├── system_monitor_agent/          # 主系統監控代理套件
│   ├── __init__.py                # 套件初始化
│   ├── agent.py                   # 代理定義 (root_agent)
│   │
│   └── subagents/                 # 子代理資料夾
│       ├── __init__.py            # 子代理初始化
│       │
│       ├── cpu_info_agent/        # CPU 資訊代理
│       │   ├── __init__.py
│       │   ├── agent.py
│       │   └── tools.py           # CPU 資訊收集工具
│       │
│       ├── memory_info_agent/     # 記憶體資訊代理
│       │   ├── __init__.py
│       │   ├── agent.py
│       │   └── tools.py           # 記憶體資訊收集工具
│       │
│       ├── disk_info_agent/       # 磁碟資訊代理
│       │   ├── __init__.py
│       │   ├── agent.py
│       │   └── tools.py           # 磁碟資訊收集工具
│       │
│       └── synthesizer_agent/     # 報告綜合代理
│           ├── __init__.py
│           └── agent.py
│
├── .env.example                   # 環境變數範例
└── README.md                      # 此文件
```

## 開始使用

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

2. 複製 `.env.example` 檔案為 `.env` 並新增您的 Google API 金鑰：
```
GOOGLE_API_KEY=your_api_key_here
```

### 執行範例

```bash
cd 10-parallel-agent
adk web
```

然後在網頁 UI 的下拉選單中選擇「system_monitor_agent」。

## 範例互動

嘗試這些範例提示：

```
檢查我的系統健康狀況
```

```
提供包含建議的全面系統報告
```

```
我的系統是否記憶體或磁碟空間不足？
```

## 關鍵概念：獨立執行

並行代理的一個關鍵方面是**子代理在執行期間獨立運行，不共享狀態**。在此範例中：

1. 每個資訊收集代理都獨立運作
2. 並行執行完成後收集每個代理的結果
3. 綜合代理然後使用這些收集的結果建立最終報告

此方法非常適合任務完全獨立且在執行期間不需要互動的場景。

## 並行代理與其他工作流程代理的比較

ADK 為不同需求提供不同類型的工作流程代理：

- **順序代理**：用於嚴格的有序執行，每個步驟都依賴前一個輸出
- **迴圈代理**：用於基於條件重複執行子代理
- **並行代理**：用於獨立子代理的並發執行（如此範例）

## 其他資源

- [ADK 並行代理文件](https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/)
- [完整範例：並行網路研究](https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/#full-example-parallel-web-research)
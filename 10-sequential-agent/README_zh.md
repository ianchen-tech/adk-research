# ADK 中的順序代理

此範例展示如何在代理開發套件 (ADK) 中實作順序代理。此範例中的主代理 `lead_qualification_agent` 是一個順序代理，按預定義順序執行子代理，每個代理的輸出都會傳遞給序列中的下一個代理。

## 什麼是順序代理？

順序代理是 ADK 中的工作流程代理，具有以下特點：

1. **按固定順序執行**：子代理按照指定的確切順序依次執行
2. **在代理間傳遞資料**：使用狀態管理將資訊從一個子代理傳遞到下一個
3. **建立處理管線**：非常適合每個步驟都依賴前一步驟輸出的場景

當您需要確定性的逐步工作流程且執行順序很重要時，請使用順序代理。

## 潛在客戶資格管線範例

在此範例中，我們建立了 `lead_qualification_agent` 作為順序代理，為銷售團隊實作潛在客戶資格管線。此順序代理協調三個專業子代理：

1. **潛在客戶驗證代理**：檢查潛在客戶資訊是否足夠完整以進行資格評估
   - 驗證必要資訊，如聯絡詳情和興趣
   - 輸出簡單的「有效」或「無效」及原因

2. **潛在客戶評分代理**：對有效潛在客戶進行 1-10 分評分
   - 分析緊急性、決策權威、預算和時間表等因素
   - 提供數字分數和簡要理由

3. **行動建議代理**：根據驗證和評分建議下一步行動
   - 對於無效潛在客戶：建議需要收集什麼資訊
   - 對於低分潛在客戶（1-3）：建議培養行動
   - 對於中等分數潛在客戶（4-7）：建議資格評估行動
   - 對於高分潛在客戶（8-10）：建議銷售行動

### 運作方式

`lead_qualification_agent` 順序代理透過以下方式協調此流程：

1. 首先執行驗證器以確定潛在客戶是否完整
2. 接著執行評分器（可透過狀態存取驗證結果）
3. 最後執行建議器（可存取驗證和評分結果）

每個子代理的輸出都使用 `output_key` 參數儲存在會話狀態中：
- `validation_status`
- `lead_score`
- `action_recommendation`

## 專案結構

```
9-sequential-agent/
│
├── lead_qualification_agent/       # 主順序代理套件
│   ├── __init__.py                 # 套件初始化
│   ├── agent.py                    # 順序代理定義 (root_agent)
│   │
│   └── subagents/                  # 子代理資料夾
│       ├── __init__.py             # 子代理初始化
│       │
│       ├── validator/              # 潛在客戶驗證代理
│       │   ├── __init__.py
│       │   └── agent.py
│       │
│       ├── scorer/                 # 潛在客戶評分代理
│       │   ├── __init__.py
│       │   └── agent.py
│       │
│       └── recommender/            # 行動建議代理
│           ├── __init__.py
│           └── agent.py
│
├── .env.example                    # 環境變數範例
└── README.md                       # 此文件
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
cd 9-sequential-agent
adk web
```

然後在網頁 UI 的下拉選單中選擇「lead_qualification_agent」。

## 範例互動

嘗試這些範例互動：

### 合格潛在客戶範例：
```
潛在客戶資訊：
姓名：Sarah Johnson
電子郵件：sarah.j@techinnovate.com
電話：555-123-4567
公司：Tech Innovate Solutions
職位：技術長
興趣：尋找 AI 解決方案來自動化客戶支援
預算：$50K-100K 可用於合適的解決方案
時間表：希望在下一季內實施
備註：目前使用競爭對手的產品但對效能不滿意
```

### 不合格潛在客戶範例：
```
潛在客戶資訊：
姓名：John Doe
電子郵件：john@gmail.com
興趣：可能與 AI 相關的東西
備註：在會議上遇到，似乎有興趣但對需求很模糊
```

## 順序代理與其他工作流程代理的比較

ADK 為不同需求提供不同類型的工作流程代理：

- **順序代理**：用於嚴格的有序執行（如此範例）
- **迴圈代理**：用於基於條件重複執行子代理
- **並行代理**：用於獨立子代理的並發執行

## 其他資源

- [ADK 順序代理文件](https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/)
- [完整程式碼開發管線範例](https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/#full-example-code-development-pipeline)
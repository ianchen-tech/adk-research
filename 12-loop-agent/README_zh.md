# LinkedIn 貼文生成器迴圈代理

此範例展示在代理開發套件 (ADK) 中使用順序和迴圈代理模式來生成和優化 LinkedIn 貼文。

## 概述

LinkedIn 貼文生成器使用帶有迴圈組件的順序管線來：
1. 生成初始 LinkedIn 貼文
2. 反覆優化貼文直到滿足品質要求

這展示了幾個關鍵模式：
1. **順序管線**：具有不同階段的多步驟工作流程
2. **反覆優化**：使用迴圈重複優化內容
3. **自動品質檢查**：根據特定標準驗證內容
4. **回饋驅動優化**：基於特定回饋改善內容
5. **迴圈退出工具**：使用工具在滿足品質要求時終止迴圈

## 架構

系統由以下組件組成：

### 根順序代理

`LinkedInPostGenerationPipeline` - 協調整體流程的順序代理：
1. 首先執行初始貼文生成器
2. 然後執行優化迴圈

### 初始貼文生成器

`InitialPostGenerator` - 在沒有先前上下文的情況下建立 LinkedIn 貼文初稿的 LlmAgent。

### 優化迴圈

`PostRefinementLoop` - 執行兩階段優化流程的迴圈代理：
1. 首先執行審查者評估貼文並可能退出迴圈
2. 如果迴圈繼續，則執行優化器改善貼文

### 優化迴圈內的子代理

1. **貼文審查者** (`PostReviewer`) - 審查貼文品質並提供回饋，或在滿足要求時退出迴圈
2. **貼文優化器** (`PostRefiner`) - 基於回饋優化貼文以提升品質

### 工具

1. **字元計數器** - 根據要求驗證貼文長度（審查者使用）
2. **退出迴圈** - 在滿足所有品質標準時終止迴圈（審查者使用）

## 使用退出工具控制迴圈

此範例中的關鍵設計模式是使用 `exit_loop` 工具來控制迴圈何時終止。貼文審查者有兩個職責：

1. **品質評估**：檢查貼文是否滿足所有要求
2. **迴圈控制**：當貼文通過所有品質檢查時呼叫 exit_loop 工具

當呼叫 exit_loop 工具時：
1. 它設定 `tool_context.actions.escalate = True`
2. 這向迴圈代理發出應該停止迭代的信號

此方法遵循 ADK 最佳實務：
1. 將初始生成與優化分離
2. 讓品質審查者直接控制迴圈終止
3. 使用專用代理進行貼文優化
4. 使用工具管理迴圈控制流程

## 使用方法

要執行此範例：

```bash
cd 11-loop-agent
adk web
```

然後在網頁介面中，輸入類似以下的提示：
"Generate a LinkedIn post about what I've learned from @aiwithbrandon's Agent Development Kit tutorial."

系統將：
1. 生成初始 LinkedIn 貼文
2. 審查貼文的品質和合規性
3. 如果貼文滿足所有要求，退出迴圈
4. 否則，提供回饋並優化貼文
5. 繼續此流程直到建立滿意的貼文或達到最大迭代次數
6. 返回最終貼文

## 範例輸入

```
Generate a LinkedIn post about what I've learned from @aiwithbrandon's Agent Development Kit tutorial.
```

## 迴圈終止

迴圈以兩種方式之一終止：
1. 當貼文滿足所有品質要求時（審查者呼叫 exit_loop 工具）
2. 達到最大迭代次數後（10 次）
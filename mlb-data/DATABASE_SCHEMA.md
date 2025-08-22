
---

## Table 1: pitching_game_logs (投手逐場記錄)

### Table 描述
儲存大谷翔平每場比賽的投手表現數據，包含投球局數、三振、防禦率等關鍵指標。

**適用情境：**
- 分析大谷翔平的投手表現趨勢和穩定性
- 評估特定對手或主客場對投球表現的影響
- 追蹤投手狀態變化（如防禦率、WHIP值的波動）
- 研究投球局數與表現品質的關聯性
- 比較不同時期的投手數據（如賽季初期vs後期）
- 分析勝負投與投手數據的相關性
- 製作投手表現報告或數據視覺化

### Schema 定義
```sql
CREATE TABLE pitching_game_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recent_game_rank INTEGER,
    opponent TEXT,
    score TEXT,
    game_type TEXT,
    decision TEXT,
    innings_pitched REAL,
    hits_allowed INTEGER,
    runs_allowed INTEGER,
    earned_runs INTEGER,
    walks INTEGER,
    strikeouts INTEGER,
    home_runs_allowed INTEGER,
    era REAL,
    whip REAL,
    baa REAL
);
```

### 欄位說明

| 欄位名稱 | 資料類型 | 說明 | 範例 |
|---------|---------|------|------|
| `id` | INTEGER | 主鍵，自動遞增 | 1, 2, 3... |
| `recent_game_rank` | INTEGER | 最近第幾場比賽（1=最近第1場） | 1, 2, 3... |
| `opponent` | TEXT | 對戰球隊（'@'開頭表示在客場比賽） | "@落磯", "教士", "天使" |
| `score` | TEXT | 比賽比分 | "敗 3-8", "勝 11-4" |
| `game_type` | TEXT | 比賽類型 | "Reg"（例行賽） |
| `decision` | TEXT | 投手勝負記錄 | "L"（敗投）, "W"（勝投）, "-"（無關勝負） |
| `innings_pitched` | REAL | 投球局數 | 4.0, 5.1, 6.2 |
| `hits_allowed` | INTEGER | 被安打數 | 5, 3, 7 |
| `runs_allowed` | INTEGER | 失分 | 2, 0, 4 |
| `earned_runs` | INTEGER | 自責分 | 2, 0, 3 |
| `walks` | INTEGER | 四壞球 | 1, 3, 0 |
| `strikeouts` | INTEGER | 三振數 | 8, 12, 5 |
| `home_runs_allowed` | INTEGER | 被全壘打數 | 0, 1, 2 |
| `era` | REAL | 防禦率 | 2.50, 3.47, 4.61 |
| `whip` | REAL | WHIP值（每局被上壘率） | 1.20, 0.95, 1.45 |
| `baa` | REAL | 被打擊率 | 0.250, 0.180, 0.320 |

### 資料範例
```sql
INSERT INTO pitching_game_logs VALUES (
    1, 1, '@落磯', '敗 3-8', 'Reg', 'L', 
    4.0, 9, 5, 5, 0, 3, 0, 4.61, 1.28, 0.278
);
```
---

### 時間排序
- `recent_game_rank` 欄位表示最近第幾場比賽
- 數值 1 = 最近第 1 場（最新的比賽）
- 數值越大表示越早期的比賽
- 資料按時間倒序排列（最新在前）

---

## Table 2: batting_game_logs (打擊逐場記錄)

### Table 描述
儲存大谷翔平每場比賽的打擊表現數據，包含打數、安打、全壘打、打點等關鍵指標。

**適用情境：**
- 追蹤打擊手感和狀態起伏
- 分析對特定球隊的打擊表現
- 評估主客場對打擊成績的影響
- 研究打擊率、上壘率、長打率的變化趨勢
- 分析全壘打產出的週期性和爆發力
- 評估關鍵時刻的打點貢獻
- 製作打擊成績報告和績效分析
- 預測未來打擊表現或設定目標

### Schema 定義
```sql
CREATE TABLE batting_game_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recent_game_rank INTEGER,
    opponent TEXT,
    score TEXT,
    game_type TEXT,
    at_bats INTEGER,
    runs INTEGER,
    hits INTEGER,
    doubles INTEGER,
    triples INTEGER,
    home_runs INTEGER,
    rbis INTEGER,
    walks INTEGER,
    strikeouts INTEGER,
    stolen_bases INTEGER,
    caught_stealing INTEGER,
    batting_avg REAL,
    obp REAL,
    slg REAL,
    ops REAL
);
```

### 欄位說明

| 欄位名稱 | 資料類型 | 說明 | 範例 |
|---------|---------|------|------|
| `id` | INTEGER | 主鍵，自動遞增 | 1, 2, 3... |
| `recent_game_rank` | INTEGER | 最近第幾場比賽（1=最近第1場） | 1, 2, 3... |
| `opponent` | TEXT | 對戰球隊（'@'開頭表示在客場比賽） | "@落磯", "教士", "天使" |
| `score` | TEXT | 比賽比分 | "敗 3-8", "勝 11-4" |
| `game_type` | TEXT | 比賽類型 | "Reg"（例行賽） |
| `at_bats` | INTEGER | 打數 | 4, 5, 3 |
| `runs` | INTEGER | 得分 | 1, 0, 2 |
| `hits` | INTEGER | 安打數 | 2, 1, 3 |
| `doubles` | INTEGER | 二壘安打 | 0, 1, 2 |
| `triples` | INTEGER | 三壘安打 | 0, 0, 1 |
| `home_runs` | INTEGER | 全壘打 | 1, 0, 2 |
| `rbis` | INTEGER | 打點 | 2, 0, 3 |
| `walks` | INTEGER | 四壞球 | 1, 0, 2 |
| `strikeouts` | INTEGER | 三振 | 1, 2, 0 |
| `stolen_bases` | INTEGER | 盜壘成功 | 0, 1, 0 |
| `caught_stealing` | INTEGER | 盜壘失敗 | 0, 0, 1 |
| `batting_avg` | REAL | 打擊率 | 0.285, 0.300, 0.275 |
| `obp` | REAL | 上壘率 | 0.393, 0.420, 0.350 |
| `slg` | REAL | 長打率 | 0.625, 0.580, 0.700 |
| `ops` | REAL | OPS值（上壘率+長打率） | 1.018, 1.000, 1.050 |

### 資料範例
```sql
INSERT INTO batting_game_logs VALUES (
    1, 1, '@落磯', '敗 3-8', 'Reg', 
    2, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 
    0.285, 0.393, 0.625, 1.018
);
```

---

### 時間排序
- `recent_game_rank` 欄位表示最近第幾場比賽
- 數值 1 = 最近第 1 場（最新的比賽）
- 數值越大表示越早期的比賽
- 資料按時間倒序排列（最新在前）

---

## Table 3: batting_season_stats (賽季打擊數據)

### Table 描述
儲存大谷翔平每個賽季的打擊統計數據，包含全壘打、打點、打擊率等年度累計指標。

**適用情境：**
- 分析大谷翔平的打擊生涯發展軌跡
- 比較不同賽季的打擊表現變化
- 評估年度打擊成績和里程碑達成
- 研究球隊轉換對打擊數據的影響
- 製作生涯打擊統計報告
- 預測未來賽季打擊表現
- 分析打擊三圍（打擊率、上壘率、長打率）的年度變化
- 追蹤全壘打和打點的年度產出

### Schema 定義
```sql
CREATE TABLE batting_season_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    season INTEGER,
    team TEXT,
    games INTEGER,
    doubles INTEGER,
    triples INTEGER,
    home_runs INTEGER,
    rbis INTEGER,
    stolen_bases INTEGER,
    avg REAL,
    caught_stealing INTEGER,
    obp REAL,
    walks INTEGER,
    slg REAL,
    ops REAL,
    strikeouts INTEGER,
    grounded_into_dp INTEGER,
    at_bats INTEGER,
    runs INTEGER
);
```

### 欄位說明

| 欄位名稱 | 資料類型 | 說明 | 範例 |
|---------|---------|------|------|
| `id` | INTEGER | 主鍵，自動遞增 | 1, 2, 3... |
| `season` | INTEGER | 賽季年份 | 2021, 2022, 2023 |
| `team` | TEXT | 所屬球隊 | "天使", "道奇" |
| `games` | INTEGER | 出賽場次 | 155, 157, 135 |
| `doubles` | INTEGER | 二壘安打數 | 26, 34, 38 |
| `triples` | INTEGER | 三壘安打數 | 8, 5, 3 |
| `home_runs` | INTEGER | 全壘打數 | 46, 34, 44 |
| `rbis` | INTEGER | 打點數 | 100, 95, 96 |
| `stolen_bases` | INTEGER | 盜壘成功數 | 26, 11, 20 |
| `avg` | REAL | 打擊率 | 0.273, 0.283, 0.304 |
| `caught_stealing` | INTEGER | 盗壘失敗數 | 8, 4, 6 |
| `obp` | REAL | 上壘率 | 0.372, 0.343, 0.412 |
| `walks` | INTEGER | 四壞球數 | 96, 64, 81 |
| `slg` | REAL | 長打率 | 0.592, 0.519, 0.654 |
| `ops` | REAL | OPS值（上壘率+長打率） | 0.965, 0.875, 1.066 |
| `strikeouts` | INTEGER | 三振數 | 189, 219, 215 |
| `grounded_into_dp` | INTEGER | 雙殺打數 | 21, 15, 18 |
| `at_bats` | INTEGER | 打數 | 537, 520, 497 |
| `runs` | INTEGER | 得分數 | 103, 90, 96 |

### 資料範例
```sql
INSERT INTO batting_season_stats VALUES (
    1, 2021, '天使', 158, 26, 8, 46, 100, 26, 
    0.273, 8, 0.372, 96, 0.592, 0.965, 189, 21, 537, 103
);
```

---

## Table 4: pitching_season_stats (賽季投球數據)

### Table 描述
儲存大谷翔平每個賽季的投手統計數據，包含勝負場次、防禦率、三振數等年度累計指標。

**適用情境：**
- 分析大谷翔平的投手生涯發展軌跡
- 比較不同賽季的投手表現變化
- 評估年度投手成績和獎項競爭力
- 研究球隊轉換對投手數據的影響
- 製作生涯投手統計報告
- 預測未來賽季投手表現
- 分析投手三大指標（防禦率、WHIP、被打擊率）的年度變化
- 追蹤勝場數和三振數的年度產出

### Schema 定義
```sql
CREATE TABLE pitching_season_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    season INTEGER,
    team TEXT,
    games INTEGER,
    earned_runs INTEGER,
    holds INTEGER,
    blown_saves INTEGER,
    games_started INTEGER,
    home_runs_allowed INTEGER,
    complete_games INTEGER,
    shutouts INTEGER,
    innings_pitched REAL,
    saves INTEGER,
    walks INTEGER,
    era REAL,
    whip REAL,
    baa REAL,
    strikeouts INTEGER,
    hits_allowed INTEGER,
    wins INTEGER,
    losses INTEGER,
    runs_allowed INTEGER
);
```

### 欄位說明

| 欄位名稱 | 資料類型 | 說明 | 範例 |
|---------|---------|------|------|
| `id` | INTEGER | 主鍵，自動遞增 | 1, 2, 3... |
| `season` | INTEGER | 賽季年份 | 2021, 2022, 2023 |
| `team` | TEXT | 所屬球隊 | "天使", "道奇" |
| `games` | INTEGER | 出賽場次 | 28, 23, 20 |
| `earned_runs` | INTEGER | 自責分數 | 44, 29, 38 |
| `holds` | INTEGER | 中繼成功數 | 0, 0, 0 |
| `blown_saves` | INTEGER | 救援失敗數 | 0, 0, 0 |
| `games_started` | INTEGER | 先發場次 | 23, 28, 20 |
| `home_runs_allowed` | INTEGER | 被全壘打數 | 14, 11, 15 |
| `complete_games` | INTEGER | 完投場次 | 0, 1, 0 |
| `shutouts` | INTEGER | 完封場次 | 0, 1, 0 |
| `innings_pitched` | REAL | 投球局數 | 130.1, 166.0, 132.0 |
| `saves` | INTEGER | 救援成功數 | 0, 0, 0 |
| `walks` | INTEGER | 四壞球數 | 44, 44, 32 |
| `era` | REAL | 防禦率 | 3.18, 2.33, 3.14 |
| `whip` | REAL | WHIP值（每局被上壘率） | 1.09, 1.01, 1.05 |
| `baa` | REAL | 被打擊率 | 0.190, 0.205, 0.184 |
| `strikeouts` | INTEGER | 三振數 | 156, 219, 167 |
| `hits_allowed` | INTEGER | 被安打數 | 98, 127, 105 |
| `wins` | INTEGER | 勝場數 | 9, 15, 10 |
| `losses` | INTEGER | 敗場數 | 2, 9, 5 |
| `runs_allowed` | INTEGER | 失分數 | 51, 35, 43 |

### 資料範例
```sql
INSERT INTO pitching_season_stats VALUES (
    1, 2021, '天使', 23, 44, 0, 0, 23, 14, 0, 0, 
    130.1, 0, 44, 3.18, 1.09, 0.190, 156, 98, 9, 2, 51
);
```

---
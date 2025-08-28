# 大谷翔平數據庫查詢範例

本檔案提供大谷翔平棒球數據庫的詳細查詢範例，涵蓋各種查詢情境和分析需求。

## 目錄
1. [基本單表查詢](#基本單表查詢)
2. [統計分析查詢](#統計分析查詢)
3. [條件篩選查詢](#條件篩選查詢)
4. [跨表關聯查詢](#跨表關聯查詢)
5. [時間序列分析](#時間序列分析)
6. [進階分析查詢](#進階分析查詢)
7. [排名與比較查詢](#排名與比較查詢)

---

## 基本單表查詢

### 1.1 查看最近投手表現
**使用情境：** 了解大谷翔平最近的投手狀態，評估當前表現水準。這個查詢特別適用於賽季中期或關鍵時刻，當教練團、球迷或分析師需要快速掌握大谷翔平的投手近況時使用。透過觀察最近幾場比賽的表現，可以判斷他是否處於良好的投球狀態，是否適合在重要比賽中擔任先發投手，或者是否需要調整投球策略。此查詢也有助於媒體記者撰寫賽前分析報導，以及球迷了解偶像的最新表現動態。

```sql
-- 查看最近5場投手表現
SELECT 
    recent_game_rank,
    opponent,
    innings_pitched,
    strikeouts,
    era,
    whip,
    decision
FROM pitching_game_logs 
ORDER BY recent_game_rank ASC 
LIMIT 5;
```

**說明：** 此查詢按時間順序顯示最近5場投手表現，包含關鍵指標如投球局數、三振數、防禦率等，有助於快速評估投手近況。recent_game_rank 欄位確保我們獲得的是最新的比賽數據，而不是隨機的5場比賽。ERA（防禦率）和WHIP（每局被上壘率）是評估投手表現的核心指標，三振數則反映了投手的壓制力。decision 欄位顯示勝負責任，有助於了解投手對球隊勝利的貢獻。這些數據組合起來，能夠提供投手狀態的全面快照，是進行後續深入分析的基礎。

### 1.2 查看最近打擊表現
**使用情境：** 追蹤打擊手感和狀態變化。打擊表現往往比投手表現更容易出現短期波動，因此定期監控最近的打擊數據對於理解大谷翔平的攻擊狀態至關重要。這個查詢適用於分析師評估他是否正處於「熱區」（hot streak）或「冷卻期」（cold streak），教練團決定打線安排，以及球迷追蹤偶像的打擊表現。特別是在季後賽或關鍵系列賽期間，最近的打擊表現往往比整季統計更具參考價值，因為它反映了球員當前的競技狀態和信心水準。

```sql
-- 查看最近5場打擊表現
SELECT 
    recent_game_rank,
    opponent,
    at_bats,
    hits,
    home_runs,
    rbis,
    batting_avg,
    ops
FROM batting_game_logs 
ORDER BY recent_game_rank ASC 
LIMIT 5;
```

**說明：** 顯示最近5場打擊數據，重點關注打擊率和OPS值的變化趨勢。at_bats（打數）和hits（安打數）是計算打擊率的基礎數據，而home_runs（全壘打）和rbis（打點）則直接反映攻擊貢獻。batting_avg（打擊率）提供即時的安打成功率，而OPS（上壘率加長打率）則是更全面的攻擊指標，結合了上壘能力和長打威力。透過觀察這些指標在最近幾場比賽中的變化，可以識別出打擊狀態的趨勢，例如是否正在回溫、是否遭遇低潮，或者是否維持穩定的高水準表現。

### 1.3 打擊賽季統計概覽
**使用情境：** 評估各賽季打擊表現和攻擊貢獻。這個查詢適用於年度打擊績效評估、打者價值分析、媒體製作打擊專題報導，以及球迷追蹤偶像的打擊發展軌跡。對於球團管理層而言，這些數據有助於評估打者的市場價值和薪資談判參考。對於打擊教練，可以識別出表現趨勢和需要調整的技術環節。

```sql
-- 打擊賽季統計
SELECT 
    season,
    team,
    games,
    home_runs,
    rbis,
    avg,
    ops
FROM batting_season_stats 
ORDER BY season DESC;
```

**說明：** 提供各賽季打擊核心數據概覽，便於進行年度間比較。查詢從batting_season_stats表格提取數據，關注games（出賽場次）、home_runs（全壘打）、rbis（打點）、avg（打擊率）和ops（攻擊指數）等關鍵指標。這些數據能夠反映出每個賽季的攻擊貢獻和打擊穩定性。透過DESC排序，最新賽季的數據會優先顯示，便於追蹤最近的打擊表現變化。

### 1.4 投手賽季統計概覽
**使用情境：** 評估各賽季投手表現和工作負荷。這個查詢適用於年度投手績效評估、先發輪值規劃、投手健康狀況監控，以及制定來季投球策略。對於投手教練而言，這些數據有助於分析投球效率和耐久性。對於醫療團隊，可以評估工作量對球員健康的影響。對於對手球隊，這是制定打擊策略的重要參考資料。

```sql
-- 投手賽季統計
SELECT 
    season,
    team,
    games_started,
    wins,
    losses,
    era,
    strikeouts,
    innings_pitched
FROM pitching_season_stats 
ORDER BY season DESC;
```

**說明：** 提供各賽季投手核心數據概覽，便於進行年度間比較。查詢從pitching_season_stats表格提取數據，聚焦於games_started（先發場次）、wins/losses（勝敗紀錄）、era（防禦率）、strikeouts（三振）和innings_pitched（投球局數）等核心數據。這些指標展現投手的工作量、勝負貢獻和投球效率。透過DESC排序，最新賽季的數據會優先顯示，便於追蹤最近的投手表現變化。

---

## 統計分析查詢

### 2.1 投手表現統計分析
**使用情境：** 深入分析投手整體表現水準和穩定性。這個綜合統計查詢適用於季末總結、年度獎項評選參考、球員交易評估，以及深度棒球分析報告的撰寫。對於投手教練而言，這些統計數據有助於識別大谷翔平的投球優勢和需要改進的領域。對於對手球隊的打擊教練，這些數據提供了制定對戰策略的重要參考。此外，這類統計分析也是棒球研究學者進行比較研究和歷史分析的重要工具，可以將大谷翔平的表現與其他頂級投手進行客觀比較。

```sql
-- 投手綜合統計分析
SELECT 
    COUNT(*) as total_games,
    ROUND(AVG(era), 2) as avg_era,
    ROUND(MIN(era), 2) as best_era,
    ROUND(MAX(era), 2) as worst_era,
    SUM(strikeouts) as total_strikeouts,
    ROUND(AVG(strikeouts), 1) as avg_strikeouts_per_game,
    ROUND(SUM(innings_pitched), 1) as total_innings,
    ROUND(AVG(innings_pitched), 1) as avg_innings_per_start,
    COUNT(CASE WHEN decision = 'W' THEN 1 END) as wins,
    COUNT(CASE WHEN decision = 'L' THEN 1 END) as losses
FROM pitching_game_logs;
```

**說明：** 提供投手表現的全面統計分析，包含平均值、極值、累計數據等，有助於評估整體投手能力。查詢使用多種聚合函數來計算不同層面的統計指標：COUNT(*)統計總出賽場次，AVG()、MIN()、MAX()函數分別計算防禦率的平均值、最佳值和最差值，展現表現的穩定性和變化範圍。SUM()函數累計三振數和投球局數，反映整體工作量和壓制力。透過CASE WHEN條件統計勝負場次，提供勝率相關資訊。這些多維度的統計數據組合，能夠建構出大谷翔平投手能力的完整輪廓，包括他的平均水準、最佳表現潛力、穩定性以及對球隊勝利的貢獻度。

### 2.2 打擊表現統計分析
**使用情境：** 評估打擊能力的各項指標和一致性。這個全面的打擊統計分析對於評估大谷翔平作為指定打擊或野手的價值具有重要意義。適用於球團制定薪資策略、媒體撰寫深度分析報導、球迷了解偶像的攻擊威力，以及對手球隊制定投球策略。對於打擊教練而言，這些數據有助於識別大谷翔平的打擊優勢區域和改進空間。此外，這類統計也是評選年度最佳指定打擊、銀棒獎等獎項的重要參考依據，以及進行歷史比較和生涯里程碑追蹤的基礎數據。

```sql
-- 打擊綜合統計分析
SELECT 
    COUNT(*) as total_games,
    SUM(at_bats) as total_at_bats,
    SUM(hits) as total_hits,
    ROUND(CAST(SUM(hits) AS FLOAT) / SUM(at_bats), 3) as overall_avg,
    SUM(home_runs) as total_home_runs,
    SUM(rbis) as total_rbis,
    ROUND(AVG(ops), 3) as avg_ops,
    COUNT(CASE WHEN home_runs > 0 THEN 1 END) as games_with_hr,
    COUNT(CASE WHEN hits >= 2 THEN 1 END) as multi_hit_games
FROM batting_game_logs;
```

**說明：** 計算打擊的累計統計和平均表現，特別關注多安打場次和全壘打頻率。查詢透過SUM()函數累計at_bats（總打數）、hits（總安打）、home_runs（總全壘打）和rbis（總打點），提供整體攻擊貢獻的量化指標。overall_avg的計算使用CAST轉換確保精確的小數運算，反映真實的整體打擊率。AVG(ops)計算平均攻擊指數，這是評估打擊全面性的重要指標。特別值得注意的是games_with_hr和multi_hit_games的統計，前者反映長打爆發力的頻率，後者顯示穩定安打能力，這兩個指標對於評估打擊的威脅性和一致性具有重要意義。

---

## 條件篩選查詢

### 3.1 優秀表現場次篩選
**使用情境：** 找出表現突出的比賽，分析成功因素。這個查詢對於深入研究大谷翔平的巔峰表現具有重要價值，適用於投手教練分析成功投球模式、媒體製作精彩表現集錦、球迷回顧經典比賽，以及運動科學研究分析高水準表現的生理和技術特徵。透過篩選出的優秀場次，可以進一步分析當天的天氣條件、對手特徵、投球策略等因素，找出促成優異表現的關鍵要素。這類分析也有助於建立表現預測模型，協助教練團在未來比賽中制定最佳策略。

```sql
-- 優秀投手表現場次（ERA < 2.00 且三振 >= 8）
SELECT 
    recent_game_rank,
    opponent,
    innings_pitched,
    strikeouts,
    era,
    whip,
    decision
FROM pitching_game_logs 
WHERE era < 2.00 AND strikeouts >= 8
ORDER BY era ASC;
```

**說明：** 篩選出防禦率低於2.00且三振數達8次以上的優秀投手表現，用於分析成功模式。這個雙重條件確保篩選出的比賽不僅在結果上優異（低ERA），也在過程上展現壓制力（高三振）。ERA < 2.00的標準代表該場比賽的失分控制極佳，而strikeouts >= 8則顯示大谷翔平在該場比賽中展現了出色的三振能力。ORDER BY era ASC的排序讓最優秀的表現排在前面，便於快速識別歷史最佳單場表現。這種篩選方式避免了僅看結果或僅看過程的片面性，提供了更全面的優秀表現定義。

### 3.2 長打表現分析
**使用情境：** 分析長打能力和爆發力表現。長打能力是評估現代棒球攻擊威力的重要指標，這個查詢特別適用於分析大谷翔平的攻擊爆發力和關鍵時刻的得分能力。對於打擊教練而言，這些數據有助於了解大谷翔平在哪些情況下更容易產生長打，進而調整打擊策略和訓練重點。對於對手投手教練，這類分析提供了制定投球策略的重要參考，了解如何避免被大谷翔平長打攻擊。媒體也經常使用這類數據來製作長打精彩回顧和攻擊力分析報導。

```sql
-- 長打表現場次（全壘打或二壘安打以上）
SELECT 
    recent_game_rank,
    opponent,
    at_bats,
    hits,
    doubles,
    home_runs,
    rbis,
    slg,
    ops
FROM batting_game_logs 
WHERE home_runs > 0 OR doubles > 0
ORDER BY (home_runs * 4 + doubles * 2) DESC;
```

**說明：** 找出有長打表現的場次，按長打價值排序，分析長打對整體攻擊力的貢獻。WHERE條件篩選出至少有一支全壘打或二壘安打的比賽，確保關注真正的長打表現。ORDER BY子句使用創新的長打價值計算公式(home_runs * 4 + doubles * 2)，這個公式反映了全壘打和二壘安打的相對價值差異，全壘打獲得4分權重，二壘安打獲得2分權重。slg（長打率）和ops欄位提供了該場比賽的整體攻擊效率指標，有助於評估長打在整體攻擊表現中的貢獻度。這種排序方式能夠突出大谷翔平最具爆發力的攻擊表現。

### 3.3 對特定球隊表現
**使用情境：** 分析對特定對手的表現差異。不同球隊擁有不同的投手風格、球場特徵和戰術體系，因此大谷翔平對不同對手的表現可能存在顯著差異。這個查詢對於制定針對性戰術策略具有重要價值，適用於教練團準備特定系列賽、球探分析對手弱點、媒體製作對戰歷史回顧，以及球迷了解偶像對特定勁敵的表現記錄。透過這類分析，可以識別出大谷翔平特別擅長對付或相對苦手的球隊，進而調整比賽策略和心理準備。

```sql
-- 對洋基隊的打擊表現
SELECT 
    recent_game_rank,
    opponent,
    at_bats,
    hits,
    home_runs,
    rbis,
    batting_avg,
    ops
FROM batting_game_logs 
WHERE opponent LIKE '%洋基%'
ORDER BY recent_game_rank ASC;
```

**說明：** 專門分析對特定強隊的表現，有助於了解面對不同等級對手的適應能力。這個範例以洋基隊為例，使用LIKE操作符搜尋包含'洋基'的對手名稱，確保能夠匹配不同的命名格式。洋基隊作為美國聯盟的傳統強隊，對大谷翔平而言是重要的競爭對手，分析對洋基的表現具有特殊意義。ORDER BY recent_game_rank ASC確保按時間順序顯示，便於觀察表現的時間趨勢。這種針對特定對手的分析方法可以套用到任何球隊，只需修改WHERE條件中的球隊名稱即可。

---

## 跨表關聯查詢

### 4.1 賽季投打綜合表現
**使用情境：** 比較各賽季的投打平衡發展。這個查詢是分析大谷翔平獨特二刀流能力的核心工具，適用於評估他在投手和打擊兩個領域的平衡發展。對於棒球歷史學家而言，這類數據有助於將大谷翔平與貝比魯斯等歷史上的二刀流球員進行比較。對於球團管理層，這些綜合數據提供了評估大谷翔平整體價值的重要依據，特別是在考慮合約續約或交易時。媒體也經常使用這類數據來製作二刀流專題報導，展現大谷翔平在現代棒球中的獨特地位。

```sql
-- 賽季投打綜合數據
SELECT 
    bs.season,
    bs.team,
    bs.games as batting_games,
    bs.home_runs,
    bs.rbis,
    bs.avg,
    bs.ops,
    ps.games_started as pitching_starts,
    ps.wins,
    ps.losses,
    ps.era,
    ps.strikeouts,
    ROUND(ps.strikeouts / ps.innings_pitched * 9, 1) as k_per_9
FROM batting_season_stats bs
JOIN pitching_season_stats ps ON bs.season = ps.season
ORDER BY bs.season DESC;
```

**說明：** 整合各賽季的投打數據，提供完整的二刀流表現概覽，包含每9局三振率等進階指標。這個JOIN查詢以season為關聯鍵，確保投打數據來自同一賽季。batting_games和pitching_starts的對比顯示了大谷翔平在兩個角色間的時間分配。k_per_9（每9局三振率）是評估投手壓制力的標準化指標，便於跨賽季比較。透過這個查詢，可以觀察到大谷翔平是否在某些賽季更專注於投球或打擊，以及他的二刀流能力是否隨時間而進化。

### 4.2 賽季投打效率比較
**使用情境：** 比較大谷翔平在不同賽季中投手和打擊效率的相對變化。這個分析有助於了解他的職業發展重心是否有所轉移，以及在哪些賽季他在投打兩方面達到了最佳平衡。對於長期追蹤大谷翔平職業生涯的分析師而言，這類數據可以揭示他的技能發展軌跡和適應策略。

```sql
-- 賽季投打效率綜合比較
SELECT 
    bs.season,
    bs.team,
    -- 打擊效率指標
    ROUND(bs.home_runs * 1.0 / bs.games, 2) as hr_per_game,
    ROUND(bs.rbis * 1.0 / bs.games, 2) as rbi_per_game,
    bs.ops as batting_ops,
    -- 投手效率指標
    ROUND(ps.strikeouts * 1.0 / ps.games_started, 1) as k_per_start,
    ROUND(ps.innings_pitched * 1.0 / ps.games_started, 1) as ip_per_start,
    ps.era as pitching_era,
    -- 綜合效率評分
    ROUND(
        (bs.ops * 100 + (4.00 - LEAST(ps.era, 4.00)) * 25) / 2, 1
    ) as combined_efficiency_score
FROM batting_season_stats bs
JOIN pitching_season_stats ps ON bs.season = ps.season
ORDER BY combined_efficiency_score DESC;
```

**說明：** 計算各賽季的投打效率指標並建立綜合評分系統。hr_per_game和rbi_per_game標準化了打擊貢獻，k_per_start和ip_per_start則標準化了投手工作量和效率。combined_efficiency_score是一個創新的綜合指標，將OPS和ERA轉換為可比較的數值並取平均，提供了評估二刀流整體表現的量化工具。這個評分系統可以幫助識別大谷翔平的巔峰賽季和相對低潮期。

### 4.3 對手強度與投打表現關聯
**使用情境：** 分析大谷翔平面對不同強度對手時的投打表現差異。這個查詢對於制定對戰策略和評估適應能力具有重要價值。教練團可以透過這些數據了解大谷翔平在面對強隊時是否能維持高水準表現，或者是否需要特別的準備和調整。

```sql
-- 對手強度與投打表現關聯分析
WITH opponent_strength AS (
    SELECT 
        opponent,
        COUNT(*) as games_faced,
        AVG(CASE WHEN decision = 'W' THEN 1.0 ELSE 0.0 END) as win_rate_against
    FROM pitching_game_logs
    WHERE decision IN ('W', 'L')
    GROUP BY opponent
),
strength_category AS (
    SELECT 
        opponent,
        CASE 
            WHEN win_rate_against >= 0.6 THEN '弱隊'
            WHEN win_rate_against >= 0.4 THEN '中等強度'
            ELSE '強隊'
        END as opponent_category
    FROM opponent_strength
    WHERE games_faced >= 2
)
SELECT 
    sc.opponent_category,
    COUNT(DISTINCT p.recent_game_rank) as pitching_games,
    COUNT(DISTINCT b.recent_game_rank) as batting_games,
    ROUND(AVG(p.era), 2) as avg_era_vs_category,
    ROUND(AVG(p.strikeouts), 1) as avg_k_vs_category,
    ROUND(AVG(b.batting_avg), 3) as avg_ba_vs_category,
    ROUND(AVG(b.ops), 3) as avg_ops_vs_category,
    SUM(b.home_runs) as total_hrs_vs_category
FROM strength_category sc
LEFT JOIN pitching_game_logs p ON sc.opponent = p.opponent
LEFT JOIN batting_game_logs b ON sc.opponent = b.opponent
GROUP BY sc.opponent_category
ORDER BY 
    CASE 
        WHEN sc.opponent_category = '強隊' THEN 1
        WHEN sc.opponent_category = '中等強度' THEN 2
        ELSE 3
    END;
```

**說明：** 使用CTE（Common Table Expression）建立對手強度分類系統，然後分析大谷翔平對不同強度對手的表現。opponent_strength CTE根據勝率計算對手強度，strength_category CTE將對手分為三個等級。主查詢透過LEFT JOIN整合投打數據，提供面對不同強度對手時的綜合表現分析。這種分析方法可以揭示大谷翔平是否具備在高水準競爭中保持優異表現的能力。

---

## 時間序列分析

### 5.1 表現趨勢分析
**使用情境：** 追蹤表現的時間變化趨勢。時間序列分析是現代運動科學的重要工具，這個查詢特別適用於識別大谷翔平的表現週期性變化、狀態起伏模式，以及預測未來表現趨勢。對於教練團而言，這類分析有助於制定訓練週期化計畫，在球員狀態低潮時調整策略，在狀態高峰時最大化利用。對於運動心理學家，這些趨勢數據可以幫助了解球員的心理狀態變化和壓力適應能力。媒體也經常使用趨勢分析來製作球員狀態報導和表現預測文章。

```sql
-- 最近10場打擊率趨勢
SELECT 
    recent_game_rank,
    opponent,
    batting_avg,
    AVG(batting_avg) OVER (
        ORDER BY recent_game_rank DESC 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) as rolling_3_game_avg
FROM batting_game_logs 
WHERE recent_game_rank <= 10
ORDER BY recent_game_rank ASC;
```

**說明：** 使用滑動平均計算最近3場的打擊率趨勢，平滑短期波動以觀察整體走向。OVER子句配合ROWS BETWEEN創建滑動視窗，計算包含當前行和前兩行的3場比賽平均值。這種滑動平均技術能夠減少單場比賽的隨機波動影響，更清楚地顯示表現趨勢。ORDER BY recent_game_rank DESC確保視窗計算按正確的時間順序進行。rolling_3_game_avg欄位提供了平滑後的趨勢線，便於識別上升、下降或穩定的表現模式。這種分析方法在金融和運動分析中都被廣泛使用，是識別趨勢變化的有效工具。

### 5.2 賽季進展表現比較
**使用情境：** 分析賽季不同階段的表現差異和適應模式。棒球賽季漫長，球員在不同階段可能面臨不同的挑戰，如賽季初的狀態調整、中期的疲勞累積、後期的壓力增加等。這個查詢對於了解大谷翔平的賽季適應能力和持久力具有重要價值，適用於制定賽季管理策略、評估體能分配效果、預測季後賽表現，以及進行跨賽季比較分析。對於球隊醫療團隊，這些數據有助於制定傷病預防和體能維護計畫。

```sql
-- 賽季進展表現分析（以recent_game_rank分組）
SELECT 
    CASE 
        WHEN recent_game_rank <= 10 THEN '最近10場'
        WHEN recent_game_rank <= 20 THEN '第11-20場'
        WHEN recent_game_rank <= 30 THEN '第21-30場'
        ELSE '30場以前'
    END as period,
    COUNT(*) as games,
    ROUND(AVG(batting_avg), 3) as avg_batting_avg,
    SUM(home_runs) as total_hrs,
    ROUND(AVG(ops), 3) as avg_ops
FROM batting_game_logs
GROUP BY 
    CASE 
        WHEN recent_game_rank <= 10 THEN '最近10場'
        WHEN recent_game_rank <= 20 THEN '第11-20場'
        WHEN recent_game_rank <= 30 THEN '第21-30場'
        ELSE '30場以前'
    END
ORDER BY 
    CASE 
        WHEN period = '最近10場' THEN 1
        WHEN period = '第11-20場' THEN 2
        WHEN period = '第21-30場' THEN 3
        ELSE 4
    END;
```

**說明：** 將比賽按時間段分組，比較不同時期的表現差異，有助於發現狀態變化模式。CASE WHEN結構將比賽按recent_game_rank分為四個時間段，提供了賽季進展的清晰劃分。GROUP BY和ORDER BY子句確保數據按邏輯順序組織和顯示。這種分組方式可以揭示大谷翔平是否存在「慢熱型」或「後勁型」的表現特徵，以及他在賽季不同階段的穩定性。avg_batting_avg、total_hrs和avg_ops等指標的對比，能夠全面評估各時期的攻擊表現水準。這種時間段分析方法也可以套用到投手數據，進行全面的賽季進展評估。

---

## 進階分析查詢

### 6.1 效率指標分析
**使用情境：** 深入分析投打效率和品質。效率指標超越了傳統的基礎統計，提供了更精確的表現評估工具。這個查詢特別適用於進階棒球分析、球員價值評估、合約談判參考，以及與其他頂級球員的客觀比較。對於投手教練而言，三振保送比和每局三振率等指標有助於評估投球的精準度和壓制力。對於球探和分析師，這些效率指標是評估球員潛力和市場價值的重要工具。Quality Start的概念也是現代棒球評估先發投手貢獻的標準指標，反映了投手對球隊勝利的實質貢獻。

```sql
-- 投手效率分析
SELECT 
    recent_game_rank,
    opponent,
    innings_pitched,
    strikeouts,
    walks,
    ROUND(CAST(strikeouts AS FLOAT) / walks, 2) as k_bb_ratio,
    ROUND(strikeouts / innings_pitched, 2) as k_per_inning,
    CASE 
        WHEN innings_pitched >= 6 AND era <= 3.00 THEN 'Quality Start'
        ELSE 'Regular Start'
    END as start_quality
FROM pitching_game_logs
WHERE innings_pitched > 0
ORDER BY k_bb_ratio DESC;
```

**說明：** 計算三振保送比、每局三振率等效率指標，並標註優質先發，評估投球品質。k_bb_ratio（三振保送比）是評估投手控球精準度的關鍵指標，比值越高表示投手越能在避免保送的同時製造三振。k_per_inning（每局三振率）標準化了三振能力，便於跨場次比較。start_quality欄位使用棒球界標準的Quality Start定義（至少6局且ERA不超過3.00），這是評估先發投手基本貢獻的重要指標。WHERE innings_pitched > 0的條件確保只分析實際有投球的場次，避免數據異常。ORDER BY k_bb_ratio DESC的排序突出了控球最精準的表現。

### 6.2 關鍵情況表現
**使用情境：** 分析在關鍵比賽情況下的表現。環境因素對棒球表現的影響不容忽視，主客場差異是其中最重要的因素之一。這個查詢對於了解大谷翔平的適應能力和心理素質具有重要意義，適用於制定客場作戰策略、評估球員的抗壓能力、分析環境適應性，以及預測在不同環境下的表現水準。對於球隊管理層，主客場表現差異數據有助於制定賽程安排和資源分配策略。對於運動心理學研究，這類數據提供了分析環境壓力對運動表現影響的重要素材。

```sql
-- 客場vs主場表現比較
SELECT 
    CASE 
        WHEN opponent LIKE '@%' THEN '客場'
        ELSE '主場'
    END as venue,
    COUNT(*) as games,
    ROUND(AVG(batting_avg), 3) as avg_batting_avg,
    SUM(home_runs) as total_hrs,
    ROUND(AVG(ops), 3) as avg_ops,
    COUNT(CASE WHEN home_runs > 0 THEN 1 END) as hr_games
FROM batting_game_logs
GROUP BY 
    CASE 
        WHEN opponent LIKE '@%' THEN '客場'
        ELSE '主場'
    END;
```

**說明：** 比較主客場表現差異，分析環境因素對表現的影響。CASE WHEN結構透過檢查opponent欄位是否以'@'開頭來區分主客場，這是棒球數據記錄的標準格式。GROUP BY venue確保數據按主客場正確分組統計。avg_batting_avg、total_hrs、avg_ops等指標的對比可以揭示大谷翔平是否存在明顯的主客場表現差異。hr_games統計有全壘打的場次數，反映在不同環境下的長打頻率。這種分析方法可以擴展到其他環境因素，如日場夜場、不同球場、不同氣候條件等，提供全面的環境適應性評估。

---

## 排名與比較查詢

### 7.1 單場最佳表現排名
**使用情境：** 找出歷史最佳單場表現。排名分析是體育統計的經典應用，這個查詢對於製作歷史回顧、評選經典比賽、媒體製作精彩集錦，以及球迷了解偶像的巔峰時刻具有重要價值。對於棒球史學家而言，這類排名數據有助於將大谷翔平的表現放在歷史脈絡中進行評估。對於年輕球員和教練，研究頂級表現的特徵有助於設定目標和改進方向。這種排名方式也常用於年度獎項評選和名人堂資格評估的參考依據。

```sql
-- 單場最佳投手表現TOP 5
SELECT 
    recent_game_rank,
    opponent,
    innings_pitched,
    strikeouts,
    era,
    whip,
    decision,
    RANK() OVER (ORDER BY strikeouts DESC, era ASC) as performance_rank
FROM pitching_game_logs
WHERE innings_pitched >= 5
ORDER BY strikeouts DESC, era ASC
LIMIT 5;
```

**說明：** 按三振數和防禦率排名，找出最佳投手表現場次。RANK() OVER函數使用複合排序條件，優先按strikeouts DESC排序（三振數越多越好），然後按era ASC排序（防禦率越低越好）。這種排序邏輯確保了既重視壓制力（三振）也重視結果（防禦率）的平衡評估。WHERE innings_pitched >= 5的條件確保只考慮有足夠投球局數的先發表現，避免短局數救援投手的數據干擾。performance_rank欄位提供了客觀的排名數字，便於快速識別歷史最佳表現。LIMIT 5限制結果為前5名，突出真正的頂級表現。

### 7.2 賽季間表現比較
**使用情境：** 評估生涯發展軌跡和成長模式。職業運動員的生涯發展軌跡分析對於理解其技能演進、巔峰期識別、衰退預測具有重要意義。這個查詢特別適用於生涯回顧分析、合約價值評估、退休時機判斷，以及與其他球員的生涯軌跡比較。對於年輕球員的發展規劃，研究頂級球員的成長軌跡可以提供寶貴的參考。對於球團管理層，這類分析有助於制定長期投資策略和球員發展計畫。媒體也經常使用這類數據製作生涯里程碑和成就回顧專題。

```sql
-- 賽季表現排名比較
SELECT 
    season,
    team,
    home_runs,
    rbis,
    avg,
    ops,
    RANK() OVER (ORDER BY ops DESC) as ops_rank,
    RANK() OVER (ORDER BY home_runs DESC) as hr_rank,
    LAG(ops) OVER (ORDER BY season) as prev_season_ops,
    ops - LAG(ops) OVER (ORDER BY season) as ops_change
FROM batting_season_stats
ORDER BY season DESC;
```

**說明：** 比較各賽季表現並計算年度間變化，評估進步或退步趨勢。RANK() OVER函數分別按OPS和全壘打數進行排名，提供不同維度的表現評估。LAG()視窗函數計算前一賽季的OPS值，這是時間序列分析的重要技術，能夠追蹤跨年度的變化。ops_change欄位透過當前賽季OPS減去前一賽季OPS，量化了年度間的進步或退步幅度。正值表示進步，負值表示退步。這種分析方法可以識別出大谷翔平的突破年份、穩定期和可能的調整期，為理解其職業發展軌跡提供量化依據。

---

## 查詢使用建議

1. **效能優化：** 在大量數據查詢時，建議在常用的篩選欄位（如recent_game_rank、season）上建立索引
2. **數據準確性：** 注意NULL值處理，特別是在計算平均值和比率時
3. **時間範圍：** 根據分析需求調整時間範圍，避免過度寬泛或狹窄的查詢
4. **結果驗證：** 重要分析結果建議交叉驗證，確保數據邏輯正確性

---

*本查詢範例檔案涵蓋了大谷翔平數據庫的主要查詢情境，可根據具體分析需求進行調整和擴展。*
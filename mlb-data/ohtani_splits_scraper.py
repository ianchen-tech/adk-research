import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd
import time
import re

class OhtaniSplitsScraper:
    def __init__(self, db_name='ohtani_stats.db'):
        self.db_name = db_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.init_database()
    
    def init_database(self):
        """初始化資料庫表格"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # 創建打擊年度統計表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS batting_season_stats (
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
            )
        ''')
        
        # 創建投手年度統計表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pitching_season_stats (
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
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"資料庫 {self.db_name} 初始化完成")
    
    def scrape_splits_data(self):
        """爬取分類統計數據"""
        url = 'https://tw.sports.yahoo.com/mlb/players/10835/splits/'
        print(f"正在爬取分類統計數據: {url}")
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 尋找所有表格
            tables = soup.find_all('table')
            print(f"找到 {len(tables)} 個表格")
            
            batting_data = []
            pitching_data = []
            
            for table_index, table in enumerate(tables):
                print(f"\n處理第 {table_index + 1} 個表格")
                
                # 檢查表格標題或內容來判斷是打擊還是投手數據
                table_text = table.get_text().lower()
                
                if any(keyword in table_text for keyword in ['avg', 'obp', 'slg', 'ops', 'rbi']):
                    print("識別為打擊數據表格")
                    batting_data.extend(self.parse_batting_table(table))
                elif any(keyword in table_text for keyword in ['era', 'whip', 'baa', 'strikeouts', 'innings']):
                    print("識別為投手數據表格")
                    pitching_data.extend(self.parse_pitching_table(table))
            
            return batting_data, pitching_data
            
        except Exception as e:
            print(f"爬取數據時發生錯誤: {e}")
            return [], []
    
    def parse_batting_table(self, table):
        """解析打擊數據表格"""
        batting_data = []
        
        try:
            rows = table.find_all('tr')
            
            # 尋找標題行來確定欄位順序
            header_row = None
            for row in rows:
                if any(cell.get_text().strip().lower() in ['season', '年份', 'avg', 'obp'] for cell in row.find_all(['th', 'td'])):
                    header_row = row
                    break
            
            if not header_row:
                print("找不到打擊數據標題行")
                return batting_data
            
            # 解析數據行
            data_rows = [row for row in rows if row != header_row and len(row.find_all('td')) > 5]
            
            for row in data_rows:
                cells = row.find_all('td')
                if len(cells) >= 10:  # 確保有足夠的欄位
                    try:
                        # 根據圖片中的表格結構解析
                        season_text = cells[0].get_text(strip=True)
                        if season_text.isdigit():
                            data = {
                                'season': int(season_text),
                                'team': cells[1].get_text(strip=True),
                                'games': self.safe_int(cells[2].get_text(strip=True)),
                                'doubles': self.safe_int(cells[3].get_text(strip=True)),
                                'triples': self.safe_int(cells[4].get_text(strip=True)),
                                'home_runs': self.safe_int(cells[5].get_text(strip=True)),
                                'rbis': self.safe_int(cells[6].get_text(strip=True)),
                                'stolen_bases': self.safe_int(cells[7].get_text(strip=True)),
                                'avg': self.safe_float(cells[8].get_text(strip=True)),
                                'caught_stealing': self.safe_int(cells[9].get_text(strip=True)),
                                'obp': self.safe_float(cells[10].get_text(strip=True)) if len(cells) > 10 else None,
                                'walks': self.safe_int(cells[11].get_text(strip=True)) if len(cells) > 11 else None,
                                'slg': self.safe_float(cells[12].get_text(strip=True)) if len(cells) > 12 else None,
                                'ops': self.safe_float(cells[13].get_text(strip=True)) if len(cells) > 13 else None,
                                'strikeouts': self.safe_int(cells[14].get_text(strip=True)) if len(cells) > 14 else None,
                                'grounded_into_dp': self.safe_int(cells[15].get_text(strip=True)) if len(cells) > 15 else None,
                                'at_bats': self.safe_int(cells[16].get_text(strip=True)) if len(cells) > 16 else None,
                                'runs': self.safe_int(cells[17].get_text(strip=True)) if len(cells) > 17 else None
                            }
                            batting_data.append(data)
                            print(f"解析打擊數據: {data['season']} {data['team']}")
                    except Exception as e:
                        print(f"解析打擊數據行時發生錯誤: {e}")
                        continue
            
        except Exception as e:
            print(f"解析打擊表格時發生錯誤: {e}")
        
        return batting_data
    
    def parse_pitching_table(self, table):
        """解析投手數據表格"""
        pitching_data = []
        
        try:
            rows = table.find_all('tr')
            
            # 尋找標題行
            header_row = None
            for row in rows:
                if any(cell.get_text().strip().lower() in ['season', '年份', 'era', 'whip'] for cell in row.find_all(['th', 'td'])):
                    header_row = row
                    break
            
            if not header_row:
                print("找不到投手數據標題行")
                return pitching_data
            
            # 解析數據行
            data_rows = [row for row in rows if row != header_row and len(row.find_all('td')) > 5]
            
            for row in data_rows:
                cells = row.find_all('td')
                if len(cells) >= 10:  # 確保有足夠的欄位
                    try:
                        season_text = cells[0].get_text(strip=True)
                        if season_text.isdigit():
                            data = {
                                'season': int(season_text),
                                'team': cells[1].get_text(strip=True),
                                'games': self.safe_int(cells[2].get_text(strip=True)),
                                'earned_runs': self.safe_int(cells[3].get_text(strip=True)),
                                'holds': self.safe_int(cells[4].get_text(strip=True)),
                                'blown_saves': self.safe_int(cells[5].get_text(strip=True)),
                                'games_started': self.safe_int(cells[6].get_text(strip=True)),
                                'home_runs_allowed': self.safe_int(cells[7].get_text(strip=True)),
                                'complete_games': self.safe_int(cells[8].get_text(strip=True)),
                                'shutouts': self.safe_int(cells[9].get_text(strip=True)),
                                'innings_pitched': self.safe_float(cells[10].get_text(strip=True)) if len(cells) > 10 else None,
                                'saves': self.safe_int(cells[11].get_text(strip=True)) if len(cells) > 11 else None,
                                'walks': self.safe_int(cells[12].get_text(strip=True)) if len(cells) > 12 else None,
                                'era': self.safe_float(cells[13].get_text(strip=True)) if len(cells) > 13 else None,
                                'whip': self.safe_float(cells[14].get_text(strip=True)) if len(cells) > 14 else None,
                                'baa': self.safe_float(cells[15].get_text(strip=True)) if len(cells) > 15 else None,
                                'strikeouts': self.safe_int(cells[16].get_text(strip=True)) if len(cells) > 16 else None,
                                'hits_allowed': self.safe_int(cells[17].get_text(strip=True)) if len(cells) > 17 else None,
                                'wins': self.safe_int(cells[18].get_text(strip=True)) if len(cells) > 18 else None,
                                'losses': self.safe_int(cells[19].get_text(strip=True)) if len(cells) > 19 else None,
                                'runs_allowed': self.safe_int(cells[20].get_text(strip=True)) if len(cells) > 20 else None
                            }
                            pitching_data.append(data)
                            print(f"解析投手數據: {data['season']} {data['team']}")
                    except Exception as e:
                        print(f"解析投手數據行時發生錯誤: {e}")
                        continue
        
        except Exception as e:
            print(f"解析投手表格時發生錯誤: {e}")
        
        return pitching_data
    
    def safe_int(self, value):
        """安全轉換為整數"""
        try:
            # 移除逗號和其他非數字字符
            clean_value = re.sub(r'[^\d-]', '', str(value))
            return int(clean_value) if clean_value and clean_value != '-' else 0
        except:
            return 0
    
    def safe_float(self, value):
        """安全轉換為浮點數"""
        try:
            # 移除逗號但保留小數點
            clean_value = re.sub(r'[^\d.-]', '', str(value))
            return float(clean_value) if clean_value and clean_value != '-' else 0.0
        except:
            return 0.0
    
    def save_to_database(self, batting_data, pitching_data):
        """將資料存入資料庫"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            # 清空現有資料
            cursor.execute('DELETE FROM batting_season_stats')
            cursor.execute('DELETE FROM pitching_season_stats')
            
            # 插入打擊數據
            for data in batting_data:
                cursor.execute('''
                    INSERT INTO batting_season_stats (
                        season, team, games, doubles, triples, home_runs, rbis, stolen_bases,
                        avg, caught_stealing, obp, walks, slg, ops, strikeouts,
                        grounded_into_dp, at_bats, runs
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data['season'], data['team'], data['games'], data['doubles'],
                    data['triples'], data['home_runs'], data['rbis'], data['stolen_bases'],
                    data['avg'], data['caught_stealing'], data['obp'], data['walks'],
                    data['slg'], data['ops'], data['strikeouts'], data['grounded_into_dp'],
                    data['at_bats'], data['runs']
                ))
            
            # 插入投手數據
            for data in pitching_data:
                cursor.execute('''
                    INSERT INTO pitching_season_stats (
                        season, team, games, earned_runs, holds, blown_saves, games_started,
                        home_runs_allowed, complete_games, shutouts, innings_pitched,
                        saves, walks, era, whip, baa, strikeouts, hits_allowed,
                        wins, losses, runs_allowed
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data['season'], data['team'], data['games'], data['earned_runs'],
                    data['holds'], data['blown_saves'], data['games_started'],
                    data['home_runs_allowed'], data['complete_games'], data['shutouts'],
                    data['innings_pitched'], data['saves'], data['walks'], data['era'],
                    data['whip'], data['baa'], data['strikeouts'], data['hits_allowed'],
                    data['wins'], data['losses'], data['runs_allowed']
                ))
            
            conn.commit()
            print(f"成功存入 {len(batting_data)} 筆打擊年度數據和 {len(pitching_data)} 筆投手年度數據到資料庫")
            
        except Exception as e:
            print(f"存入資料庫時發生錯誤: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def run(self):
        """執行完整的爬取流程"""
        print("開始爬取大谷翔平分類統計資料...")
        
        # 爬取分類統計數據
        batting_data, pitching_data = self.scrape_splits_data()
        
        # 存入資料庫
        if batting_data or pitching_data:
            self.save_to_database(batting_data, pitching_data)
            print("爬取完成！")
        else:
            print("沒有爬取到任何資料")
    
    def query_stats(self):
        """查詢統計資料"""
        conn = sqlite3.connect(self.db_name)
        
        print("\n=== 打擊年度統計 ===")
        batting_df = pd.read_sql_query('SELECT * FROM batting_season_stats ORDER BY season DESC', conn)
        if len(batting_df) > 0:
            print(batting_df[['season', 'team', 'games', 'home_runs', 'rbis', 'avg', 'obp', 'slg', 'ops']])
            print(f"\n生涯總全壘打: {batting_df['home_runs'].sum()}")
            print(f"生涯總打點: {batting_df['rbis'].sum()}")
        
        print("\n=== 投手年度統計 ===")
        pitching_df = pd.read_sql_query('SELECT * FROM pitching_season_stats ORDER BY season DESC', conn)
        if len(pitching_df) > 0:
            print(pitching_df[['season', 'team', 'games', 'wins', 'losses', 'era', 'strikeouts', 'innings_pitched']])
            print(f"\n生涯總勝場: {pitching_df['wins'].sum()}")
            print(f"\n生涯總三振: {pitching_df['strikeouts'].sum()}")
        
        conn.close()

if __name__ == '__main__':
    # 執行爬蟲
    scraper = OhtaniSplitsScraper()
    scraper.run()
    
    # 顯示統計資料
    scraper.query_stats()
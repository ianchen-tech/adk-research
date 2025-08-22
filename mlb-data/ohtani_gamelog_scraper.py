import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd
import time

class OhtaniDataScraper:
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
        
        # 創建投手數據表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pitching_game_logs (
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
            )
        ''')
        
        # 創建打擊數據表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS batting_game_logs (
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
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"資料庫 {self.db_name} 初始化完成")
    
    def scrape_pitching_data(self):
        """爬取投手數據"""
        url = 'https://tw.sports.yahoo.com/mlb/players/10835/gamelog/?selectedTable=0'
        print(f"正在爬取投手數據: {url}")
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 尋找投手數據表格
            table = soup.find('table')
            if not table:
                print("找不到投手數據表格")
                return []
            
            rows = table.find_all('tr')[1:]  # 跳過標題行
            pitching_data = []
            
            for index, row in enumerate(rows, 1):  # 從1開始編號，第一筆是最近第一場
                cells = row.find_all('td')
                if len(cells) >= 12:  # 確保有足夠的欄位
                    try:
                        data = {
                            'recent_game_rank': index-1,  # 最近第幾場
                            'opponent': cells[1].get_text(strip=True),
                            'score': cells[2].get_text(strip=True),
                            'game_type': cells[3].get_text(strip=True),
                            'decision': cells[4].get_text(strip=True),
                            'innings_pitched': self.safe_float(cells[5].get_text(strip=True)),
                            'hits_allowed': self.safe_int(cells[6].get_text(strip=True)),
                            'runs_allowed': self.safe_int(cells[7].get_text(strip=True)),
                            'earned_runs': self.safe_int(cells[8].get_text(strip=True)),
                            'walks': self.safe_int(cells[9].get_text(strip=True)),
                            'strikeouts': self.safe_int(cells[10].get_text(strip=True)),
                            'home_runs_allowed': self.safe_int(cells[11].get_text(strip=True)),
                            'era': self.safe_float(cells[12].get_text(strip=True)) if len(cells) > 12 else None,
                            'whip': self.safe_float(cells[13].get_text(strip=True)) if len(cells) > 13 else None,
                            'baa': self.safe_float(cells[14].get_text(strip=True)) if len(cells) > 14 else None
                        }
                        pitching_data.append(data)
                    except Exception as e:
                        print(f"解析投手數據行時發生錯誤: {e}")
                        continue
            
            print(f"成功爬取 {len(pitching_data)} 筆投手數據")
            return pitching_data
            
        except Exception as e:
            print(f"爬取投手數據時發生錯誤: {e}")
            return []
    
    def scrape_batting_data(self):
        """爬取打擊數據"""
        url = 'https://tw.sports.yahoo.com/mlb/players/10835/gamelog/?selectedTable=1'
        print(f"正在爬取打擊數據: {url}")
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 尋找打擊數據表格
            table = soup.find('table')
            if not table:
                print("找不到打擊數據表格")
                return []
            
            rows = table.find_all('tr')[1:]  # 跳過標題行
            batting_data = []
            
            for index, row in enumerate(rows, 1):  # 從1開始編號，第一筆是最近第一場
                cells = row.find_all('td')
                if len(cells) >= 15:  # 確保有足夠的欄位
                    try:
                        data = {
                            'recent_game_rank': index-1,  # 最近第幾場
                            'opponent': cells[1].get_text(strip=True),
                            'score': cells[2].get_text(strip=True),
                            'game_type': cells[3].get_text(strip=True),
                            'at_bats': self.safe_int(cells[4].get_text(strip=True)),
                            'runs': self.safe_int(cells[5].get_text(strip=True)),
                            'hits': self.safe_int(cells[6].get_text(strip=True)),
                            'doubles': self.safe_int(cells[7].get_text(strip=True)),
                            'triples': self.safe_int(cells[8].get_text(strip=True)),
                            'home_runs': self.safe_int(cells[9].get_text(strip=True)),
                            'rbis': self.safe_int(cells[10].get_text(strip=True)),
                            'walks': self.safe_int(cells[11].get_text(strip=True)),
                            'strikeouts': self.safe_int(cells[12].get_text(strip=True)),
                            'stolen_bases': self.safe_int(cells[13].get_text(strip=True)),
                            'caught_stealing': self.safe_int(cells[14].get_text(strip=True)),
                            'batting_avg': self.safe_float(cells[15].get_text(strip=True)) if len(cells) > 15 else None,
                            'obp': self.safe_float(cells[16].get_text(strip=True)) if len(cells) > 16 else None,
                            'slg': self.safe_float(cells[17].get_text(strip=True)) if len(cells) > 17 else None,
                            'ops': self.safe_float(cells[18].get_text(strip=True)) if len(cells) > 18 else None
                        }
                        batting_data.append(data)
                    except Exception as e:
                        print(f"解析打擊數據行時發生錯誤: {e}")
                        continue
            
            print(f"成功爬取 {len(batting_data)} 筆打擊數據")
            return batting_data
            
        except Exception as e:
            print(f"爬取打擊數據時發生錯誤: {e}")
            return []
    
    def safe_int(self, value):
        """安全轉換為整數"""
        try:
            return int(value) if value and value != '-' else 0
        except:
            return 0
    
    def safe_float(self, value):
        """安全轉換為浮點數"""
        try:
            return float(value) if value and value != '-' else 0.0
        except:
            return 0.0
    
    def save_to_database(self, pitching_data, batting_data):
        """將資料存入資料庫"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            # 清空現有資料（可選）
            cursor.execute('DELETE FROM pitching_game_logs')
            cursor.execute('DELETE FROM batting_game_logs')
            
            # 插入投手數據
            for data in pitching_data:
                cursor.execute('''
                    INSERT INTO pitching_game_logs (
                        recent_game_rank, opponent, score, game_type, decision, innings_pitched,
                        hits_allowed, runs_allowed, earned_runs, walks, strikeouts,
                        home_runs_allowed, era, whip, baa
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data['recent_game_rank'], data['opponent'], data['score'], data['game_type'],
                    data['decision'], data['innings_pitched'], data['hits_allowed'],
                    data['runs_allowed'], data['earned_runs'], data['walks'],
                    data['strikeouts'], data['home_runs_allowed'], data['era'],
                    data['whip'], data['baa']
                ))
            
            # 插入打擊數據
            for data in batting_data:
                cursor.execute('''
                    INSERT INTO batting_game_logs (
                        recent_game_rank, opponent, score, game_type, at_bats, runs, hits,
                        doubles, triples, home_runs, rbis, walks, strikeouts,
                        stolen_bases, caught_stealing, batting_avg, obp, slg, ops
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data['recent_game_rank'], data['opponent'], data['score'], data['game_type'],
                    data['at_bats'], data['runs'], data['hits'], data['doubles'],
                    data['triples'], data['home_runs'], data['rbis'], data['walks'],
                    data['strikeouts'], data['stolen_bases'], data['caught_stealing'],
                    data['batting_avg'], data['obp'], data['slg'], data['ops']
                ))
            
            conn.commit()
            print(f"成功存入 {len(pitching_data)} 筆投手數據和 {len(batting_data)} 筆打擊數據到資料庫")
            
        except Exception as e:
            print(f"存入資料庫時發生錯誤: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def run(self):
        """執行完整的爬取流程"""
        print("開始爬取大谷翔平比賽記錄...")
        
        # 爬取投手數據
        pitching_data = self.scrape_pitching_data()
        time.sleep(2)  # 避免請求過於頻繁
        
        # 爬取打擊數據
        batting_data = self.scrape_batting_data()
        
        # 存入資料庫
        if pitching_data or batting_data:
            self.save_to_database(pitching_data, batting_data)
            print("爬取完成！")
        else:
            print("沒有爬取到任何資料")
    
    def query_stats(self):
        """查詢統計資料"""
        conn = sqlite3.connect(self.db_name)
        
        print("\n=== 投手數據統計 ===")
        pitching_df = pd.read_sql_query('SELECT * FROM pitching_game_logs ORDER BY recent_game_rank ASC', conn)
        print(f"總場次: {len(pitching_df)}")
        if len(pitching_df) > 0:
            print(f"平均防禦率: {pitching_df['era'].mean():.2f}")
            print(f"總三振數: {pitching_df['strikeouts'].sum()}")
            print("\n最近5場投手表現:")
            print(pitching_df[['recent_game_rank', 'opponent', 'innings_pitched', 'strikeouts', 'era']].head())
        
        print("\n=== 打擊數據統計 ===")
        batting_df = pd.read_sql_query('SELECT * FROM batting_game_logs ORDER BY recent_game_rank ASC', conn)
        print(f"總場次: {len(batting_df)}")
        if len(batting_df) > 0:
            print(f"平均打擊率: {batting_df['batting_avg'].mean():.3f}")
            print(f"總全壘打數: {batting_df['home_runs'].sum()}")
            print(f"總打點數: {batting_df['rbis'].sum()}")
            print("\n最近5場打擊表現:")
            print(batting_df[['recent_game_rank', 'opponent', 'at_bats', 'hits', 'home_runs', 'rbis', 'batting_avg']].head())
        
        conn.close()

if __name__ == '__main__':
    # 執行爬蟲
    scraper = OhtaniDataScraper()
    scraper.run()
    
    # 顯示統計資料
    scraper.query_stats()
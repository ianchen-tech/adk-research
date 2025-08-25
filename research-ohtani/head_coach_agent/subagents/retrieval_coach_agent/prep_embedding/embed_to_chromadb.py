from dotenv import load_dotenv
import os
import chromadb
from google import genai
from typing import List, Dict, Any

current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '..', '..', '..', '.env')
load_dotenv(env_path)

class GeminiEmbedder:
    
    def __init__(self):
        """初始化 ChromaDB 和 Gemini API"""

        # 從環境變數獲取 API 金鑰
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("請設置 GEMINI_API_KEY 環境變數")
        
        # 初始化 Gemini 客戶端
        self.genai_client = genai.Client(api_key=api_key)
        
        # 創建 ChromaDB 客戶端
        self.client = chromadb.PersistentClient(path="./vector_db")
        
        # 創建文檔集合
        self.collection = self.client.get_or_create_collection(
            name="documents"
        )
    
    def get_embedding(self, text: str) -> List[float]:
        """使用 Gemini API 獲取文本嵌入向量"""
        try:
            result = self.genai_client.models.embed_content(
                model="gemini-embedding-001",
                contents=text
            )
            return result.embeddings[0].values
        except Exception as e:
            print(f"獲取嵌入向量時出錯: {e}")
            return []
    
    def add_file(self, file_path):
        """添加一個 markdown 文件到資料庫"""
        # 讀取文件內容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 獲取文件名作為 ID
        file_name = os.path.basename(file_path)
        
        # 獲取嵌入向量
        embedding = self.get_embedding(content)
        
        if embedding:
            # 添加到資料庫
            self.collection.add(
                embeddings=[embedding],
                documents=[content],
                ids=[file_name]
            )
            print(f"已添加文件: {file_name}")
        else:
            print(f"無法為文件 {file_name} 生成嵌入向量")
    
    def add_folder(self, folder_path):
        """添加整個資料夾的 markdown 文件"""
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.md'):
                file_path = os.path.join(folder_path, file_name)
                self.add_file(file_path)
    
    def search(self, question, num_results=3):
        """搜索相關文檔"""
        # 獲取查詢的嵌入向量
        query_embedding = self.get_embedding(question)
        
        if not query_embedding:
            print("無法為查詢生成嵌入向量")
            return
        
        # 在 ChromaDB 中搜索
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=num_results
        )
        
        print(f"\n搜索: '{question}'")
        print("找到的相關內容:")
        
        for i, doc in enumerate(results['documents'][0]):
            print(f"\n結果 {i+1}:")
            print(doc[:200] + "...")
    
    def show_info(self):
        """顯示資料庫信息"""
        count = self.collection.count()
        print(f"資料庫中共有 {count} 個文檔")


if __name__ == "__main__":
    # 1. 創建嵌入器
    embedder = GeminiEmbedder()
    
    # 2. 添加文檔
    schema_folder = "database_schema"
    examples_folder = "query_examples"
    
    if os.path.exists(schema_folder):
        embedder.add_folder(schema_folder)
    
    if os.path.exists(examples_folder):
        embedder.add_folder(examples_folder)
    
    # 3. 顯示資料庫信息
    embedder.show_info()
    
    # 4. 測試搜索
    embedder.search("近五場打擊率多少")
    embedder.search("去年投了幾次三振")
from dotenv import load_dotenv
import os
import chromadb
from google import genai
from google.genai import types
from chromadb import Documents, EmbeddingFunction, Embeddings

current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '..', '..', '..', '.env')
load_dotenv(env_path)

client = genai.Client()

class GeminiEmbeddingFunction(EmbeddingFunction):
    """自定義的 Gemini 嵌入函數類"""
    
    def __call__(self, input: Documents) -> Embeddings:
        """將文檔列表轉換為嵌入向量列表"""
        EMBEDDING_MODEL_ID = "gemini-embedding-001"
        response = client.models.embed_content(
            model=EMBEDDING_MODEL_ID,
            contents=input,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                title="檢索"
            )
        )
        return response.embeddings[0].values

class GeminiEmbedder:
    def __init__(self):
        """初始化 ChromaDB"""
        
        # 創建 ChromaDB 客戶端
        self.client = chromadb.PersistentClient(path="./chroma_db")
        
        # 創建文檔集合，使用自定義嵌入函數
        self.collection = self.client.get_or_create_collection(
            name="documents",
            embedding_function=GeminiEmbeddingFunction()
        )
    
    def add_file(self, file_path):
        """添加一個 markdown 文件到資料庫"""
        # 讀取文件內容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 獲取文件名作為 ID
        file_name = os.path.basename(file_path)
        
        # 添加到資料庫
        self.collection.add(
            documents=[content],
            ids=[file_name]
        )
        print(f"已添加文件: {file_name}")
    
    def add_folder(self, folder_path):
        """添加整個資料夾的 markdown 文件"""
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.md'):
                file_path = os.path.join(folder_path, file_name)
                self.add_file(file_path)
    
    def search(self, question, num_results=1):
        """搜索相關文檔"""
        # 查詢向量
        results = self.collection.query(
            query_texts=[question],
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
        print("========================")
        print(f"\n資料庫中共有 {count} 個文檔")
        
        # 如果有文檔，顯示第一筆文檔的詳細資訊
        if count > 0:
            sample_data = self.collection.get(
                limit=1, 
                include=['documents', 'embeddings', 'metadatas']
            )
            
            doc_id = sample_data['ids'][0]
            document = sample_data['documents'][0]
            embedding = sample_data['embeddings'][0]
            
            print(f"\n=== 範例文檔詳細資訊 ===")
            print(f"\n文檔 ID: {doc_id}")
            
            print(f"\n原始文本 (前 100 字符):")
            print(f"\"{document[:100]}{'...' if len(document) > 100 else ''}\"")
            print(f"完整文本長度: {len(document)} 字符")
            
            print(f"\n對應的向量值:")
            print(f"向量維度: {len(embedding)}")
            print(f"向量值 (前 20 個維度): \n{embedding[:20]}")


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

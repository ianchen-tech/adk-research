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

class SeparateGeminiEmbedder:
    def __init__(self):
        """初始化兩個不同的 ChromaDB 資料庫"""
        
        # 創建 schema_db 客戶端和集合
        self.schema_client = chromadb.PersistentClient(path="./schema_db")
        self.schema_collection = self.schema_client.get_or_create_collection(
            name="database_schema",
            embedding_function=GeminiEmbeddingFunction()
        )
        
        # 創建 examples_db 客戶端和集合
        self.examples_client = chromadb.PersistentClient(path="./examples_db")
        self.examples_collection = self.examples_client.get_or_create_collection(
            name="query_examples",
            embedding_function=GeminiEmbeddingFunction()
        )
    
    def add_file_to_schema(self, file_path):
        """添加一個 markdown 文件到 schema 資料庫"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        file_name = os.path.basename(file_path)
        
        self.schema_collection.add(
            documents=[content],
            ids=[file_name]
        )
        print(f"已添加文件到 schema_db: {file_name}")
    
    def add_file_to_examples(self, file_path):
        """添加一個 markdown 文件到 examples 資料庫"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        file_name = os.path.basename(file_path)
        
        self.examples_collection.add(
            documents=[content],
            ids=[file_name]
        )
        print(f"已添加文件到 examples_db: {file_name}")
    
    def add_schema_folder(self, folder_path):
        """添加整個 database_schema 資料夾的 markdown 文件"""
        if not os.path.exists(folder_path):
            print(f"資料夾不存在: {folder_path}")
            return
            
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.md'):
                file_path = os.path.join(folder_path, file_name)
                self.add_file_to_schema(file_path)
    
    def add_examples_folder(self, folder_path):
        """添加整個 query_examples 資料夾的 markdown 文件"""
        if not os.path.exists(folder_path):
            print(f"資料夾不存在: {folder_path}")
            return
            
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.md'):
                file_path = os.path.join(folder_path, file_name)
                self.add_file_to_examples(file_path)
    
    def search_schema(self, question, num_results=1):
        """在 schema 資料庫中搜索相關文檔"""
        results = self.schema_collection.query(
            query_texts=[question],
            n_results=num_results
        )
        
        print(f"\n在 schema_db 中搜索: '{question}'")
        print("找到的相關內容:")
        
        for i, doc in enumerate(results['documents'][0]):
            print(f"\n結果 {i+1}:")
            print(doc[:200] + "...")
    
    def search_examples(self, question, num_results=1):
        """在 examples 資料庫中搜索相關文檔"""
        results = self.examples_collection.query(
            query_texts=[question],
            n_results=num_results
        )
        
        print(f"\n在 examples_db 中搜索: '{question}'")
        print("找到的相關內容:")
        
        for i, doc in enumerate(results['documents'][0]):
            print(f"\n結果 {i+1}:")
            print(doc[:200] + "...")
    
    def search_both(self, question, num_results=1):
        """在兩個資料庫中都搜索"""
        print(f"\n=== 搜索問題: '{question}' ===")
        self.search_schema(question, num_results)
        self.search_examples(question, num_results)
    
    def show_info(self):
        """顯示兩個資料庫的信息"""
        schema_count = self.schema_collection.count()
        examples_count = self.examples_collection.count()
        
        print("========================")
        print(f"\nschema_db 中共有 {schema_count} 個文檔")
        print(f"examples_db 中共有 {examples_count} 個文檔")
        
        # 顯示 schema_db 的範例文檔
        if schema_count > 0:
            sample_data = self.schema_collection.get(
                limit=1, 
                include=['documents', 'embeddings', 'metadatas']
            )
            
            doc_id = sample_data['ids'][0]
            document = sample_data['documents'][0]
            embedding = sample_data['embeddings'][0]
            
            print(f"\n=== schema_db 範例文檔 ===")
            print(f"文檔 ID: {doc_id}")
            print(f"原始文本 (前 100 字符): \"{document[:100]}{'...' if len(document) > 100 else ''}\"")
            print(f"向量維度: {len(embedding)}")
        
        # 顯示 examples_db 的範例文檔
        if examples_count > 0:
            sample_data = self.examples_collection.get(
                limit=1, 
                include=['documents', 'embeddings', 'metadatas']
            )
            
            doc_id = sample_data['ids'][0]
            document = sample_data['documents'][0]
            embedding = sample_data['embeddings'][0]
            
            print(f"\n=== examples_db 範例文檔 ===")
            print(f"文檔 ID: {doc_id}")
            print(f"原始文本 (前 100 字符): \"{document[:100]}{'...' if len(document) > 100 else ''}\"")
            print(f"向量維度: {len(embedding)}")


if __name__ == "__main__":
    # 1. 創建分離的嵌入器
    embedder = SeparateGeminiEmbedder()
    
    # 2. 設定資料夾路徑（在同一個目錄下）
    schema_folder = "database_schema"
    examples_folder = "query_examples"
    
    # 3. 分別添加文檔到不同的資料庫
    print("正在添加 database_schema 文件到 schema_db...")
    embedder.add_schema_folder(schema_folder)
    
    print("\n正在添加 query_examples 文件到 examples_db...")
    embedder.add_examples_folder(examples_folder)
    
    # 4. 顯示資料庫信息
    embedder.show_info()
    
    # 5. 測試搜索
    print("\n=== 測試搜索功能 ===")
    embedder.search_schema("batting statistics")
    embedder.search_examples("近五場打擊率多少")
    
    # 6. 在兩個資料庫中都搜索
    embedder.search_both("投手統計")
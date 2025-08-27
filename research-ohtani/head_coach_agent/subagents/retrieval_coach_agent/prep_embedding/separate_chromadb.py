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
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=input,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                title="檢索"
            )
        )
        return response.embeddings[0].values

class GeminiEmbedder:
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
    
    def add_file(self, file_path, collection, db_name):
        """通用的添加文件方法"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        file_name = os.path.basename(file_path)
        
        collection.add(
            documents=[content],
            ids=[file_name]
        )
        print(f"已添加文件到 {db_name}: {file_name}")
    
    def add_folder(self, folder_path, db_name):
        """根據資料庫名稱添加文件到指定的 collection"""
        if db_name == "schema_db":
            collection = self.schema_collection
        elif db_name == "examples_db":
            collection = self.examples_collection
        else:
            raise ValueError(f"未知的資料庫名稱: {db_name}。支援的名稱: schema_db, examples_db")
        
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.md'):
                file_path = os.path.join(folder_path, file_name)
                self.add_file(file_path, collection, db_name)
    
    def search(self, question, db_name, num_results=1):
        """通用的搜索方法"""
        if db_name == "schema_db":
            collection = self.schema_collection
        elif db_name == "examples_db":
            collection = self.examples_collection
        else:
            raise ValueError(f"未知的資料庫名稱: {db_name}。支援的名稱: schema_db, examples_db")
        
        results = collection.query(
            query_texts=[question],
            n_results=num_results
        )
        
        print(f"\n在 {db_name} 中搜索: '{question}'")
        print("找到的相關內容:")
        
        for i, doc in enumerate(results['documents'][0]):
            print(f"\n結果 {i+1}:")
            print(doc[:200] + "...")
        
        return results
    
    def show_info(self):
        """顯示兩個資料庫的信息"""
        schema_count = self.schema_collection.count()
        examples_count = self.examples_collection.count()
        
        print("========================")
        print(f"\nschema_db 中共有 {schema_count} 個文檔")
        print(f"examples_db 中共有 {examples_count} 個文檔")
        
        # 顯示範例文檔的通用方法
        def show_sample(collection, db_name):
            if collection.count() > 0:
                sample_data = collection.get(
                    limit=1, 
                    include=['documents', 'embeddings', 'metadatas']
                )
                
                doc_id = sample_data['ids'][0]
                document = sample_data['documents'][0]
                embedding = sample_data['embeddings'][0]
                
                print(f"\n=== {db_name} 範例文檔 ===")
                print(f"文檔 ID: {doc_id}")
                print(f"原始文本 (前 100 字符): \"{document[:100]}{'...' if len(document) > 100 else ''}\"")
                print(f"向量維度: {len(embedding)}")
        
        show_sample(self.schema_collection, "schema_db")
        show_sample(self.examples_collection, "examples_db")


if __name__ == "__main__":
    # 1. 創建分離的嵌入器
    embedder = GeminiEmbedder()
    
    # 2. 設定資料夾路徑
    schema_folder = "database_schema"
    examples_folder = "query_examples"
    
    # 3. 添加文檔
    print("正在添加 database_schema 文件到 schema_db...")
    embedder.add_folder(schema_folder, "schema_db")
    
    print("\n正在添加 query_examples 文件到 examples_db...")
    embedder.add_folder(examples_folder, "examples_db")
    
    # 4. 顯示資料庫信息
    embedder.show_info()
    
    # 5. 測試搜索
    print("\n=== 測試搜索功能 ===")
    embedder.search("近五場打擊率多少", "schema_db")
    embedder.search("近五場打擊率多少", "examples_db")
    

#chromadb                                 1.0.20
#google-genai                             1.31.0
import os
import chromadb
from chromadb.config import Settings
from typing import List, Dict
import hashlib

class MarkdownEmbedder:
    def __init__(self, db_path: str = "./chroma_db"):
        """
        初始化 ChromaDB 客戶端
        
        Args:
            db_path: ChromaDB 資料庫存儲路徑
        """
        self.client = chromadb.PersistentClient(
            path=db_path,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # 創建或獲取集合
        self.collection = self.client.get_or_create_collection(
            name="ohtani_baseball_docs",
            metadata={"description": "大谷翔平棒球數據文檔嵌入"}
        )
    
    def read_markdown_file(self, file_path: str) -> str:
        """
        讀取 Markdown 檔案內容
        
        Args:
            file_path: 檔案路徑
            
        Returns:
            檔案內容字符串
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"讀取檔案 {file_path} 時發生錯誤: {e}")
            return ""
    
    def get_all_md_files(self, directory: str) -> List[str]:
        """
        獲取目錄中所有 .md 檔案的路徑
        
        Args:
            directory: 目錄路徑
            
        Returns:
            .md 檔案路徑列表
        """
        md_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.md'):
                    md_files.append(os.path.join(root, file))
        return md_files
    
    def generate_document_id(self, file_path: str) -> str:
        """
        為文檔生成唯一 ID
        
        Args:
            file_path: 檔案路徑
            
        Returns:
            文檔 ID
        """
        # 使用檔案路徑的 hash 作為 ID
        return hashlib.md5(file_path.encode()).hexdigest()
    
    def extract_metadata(self, file_path: str, content: str) -> Dict[str, str]:
        """
        從檔案路徑和內容中提取元數據
        
        Args:
            file_path: 檔案路徑
            content: 檔案內容
            
        Returns:
            元數據字典
        """
        # 確定文檔類型
        if "database_schema" in file_path:
            doc_type = "database_schema"
        elif "query_examples" in file_path:
            doc_type = "query_examples"
        else:
            doc_type = "unknown"
        
        # 提取檔案名稱（不含副檔名）
        filename = os.path.splitext(os.path.basename(file_path))[0]
        
        # 嘗試從內容中提取標題
        title = filename  # 預設使用檔案名
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        return {
            "file_path": file_path,
            "filename": filename,
            "doc_type": doc_type,
            "title": title,
            "file_size": str(len(content))
        }
    
    def embed_documents(self, schema_dir: str, examples_dir: str):
        """
        將指定目錄中的所有 .md 檔案嵌入到 ChromaDB
        每個檔案作為一個完整的文檔進行嵌入
        
        Args:
            schema_dir: database_schema 目錄路徑
            examples_dir: query_examples 目錄路徑
        """
        all_directories = [schema_dir, examples_dir]
        
        documents = []
        metadatas = []
        ids = []
        
        for directory in all_directories:
            if not os.path.exists(directory):
                print(f"目錄不存在: {directory}")
                continue
            
            md_files = self.get_all_md_files(directory)
            print(f"在 {directory} 中找到 {len(md_files)} 個 .md 檔案")
            
            for file_path in md_files:
                print(f"處理檔案: {file_path}")
                
                # 讀取檔案內容
                content = self.read_markdown_file(file_path)
                if not content:
                    continue
                
                # 提取元數據
                metadata = self.extract_metadata(file_path, content)
                
                # 為整個檔案創建一個文檔條目
                doc_id = self.generate_document_id(file_path)
                
                documents.append(content)
                metadatas.append(metadata)
                ids.append(doc_id)
        
        # 批量添加到 ChromaDB
        if documents:
            print(f"正在將 {len(documents)} 個文檔添加到 ChromaDB...")
            
            # 檢查是否已存在相同 ID 的文檔
            try:
                existing_ids = set(self.collection.get()["ids"])
                new_documents = []
                new_metadatas = []
                new_ids = []
                
                for doc, meta, doc_id in zip(documents, metadatas, ids):
                    if doc_id not in existing_ids:
                        new_documents.append(doc)
                        new_metadatas.append(meta)
                        new_ids.append(doc_id)
                
                if new_documents:
                    self.collection.add(
                        documents=new_documents,
                        metadatas=new_metadatas,
                        ids=new_ids
                    )
                    print(f"成功添加 {len(new_documents)} 個新文檔")
                else:
                    print("所有文檔都已存在，無需添加")
                    
            except Exception as e:
                print(f"添加文檔時發生錯誤: {e}")
        else:
            print("沒有找到要處理的文檔")
    
    def search_documents(self, query: str, n_results: int = 5) -> Dict:
        """
        搜索相關文檔
        
        Args:
            query: 搜索查詢
            n_results: 返回結果數量
            
        Returns:
            搜索結果
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results
        except Exception as e:
            print(f"搜索時發生錯誤: {e}")
            return {}
    
    def get_collection_info(self) -> Dict:
        """
        獲取集合信息
        
        Returns:
            集合統計信息
        """
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": self.collection.name
            }
        except Exception as e:
            print(f"獲取集合信息時發生錯誤: {e}")
            return {}

def test_search_function(embedder: MarkdownEmbedder, query: str = "打擊率", n_results: int = 3):
    """
    測試搜索功能的獨立函數
    
    Args:
        embedder: MarkdownEmbedder 實例
        query: 搜索查詢詞
        n_results: 返回結果數量
    """
    print("\n=== 測試搜索功能 ===")
    print(f"搜索查詢: '{query}'")
    
    results = embedder.search_documents(query, n_results=n_results)
    
    if results and 'documents' in results and results['documents']:
        print(f"\n找到 {len(results['documents'][0])} 個相關結果:")
        
        for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
            print(f"\n--- 結果 {i+1} ---")
            print(f"檔案: {metadata.get('filename', 'N/A')}")
            print(f"類型: {metadata.get('doc_type', 'N/A')}")
            print(f"標題: {metadata.get('title', 'N/A')}")
            print(f"內容預覽: {doc[:200]}{'...' if len(doc) > 200 else ''}")
    else:
        print("沒有找到相關結果")

def main():
    """
    主函數 - 執行嵌入過程
    """
    # 設定目錄路徑
    current_dir = os.path.dirname(os.path.abspath(__file__))
    schema_dir = os.path.join(current_dir, "database_schema")
    examples_dir = os.path.join(current_dir, "query_examples")
    
    # 創建嵌入器實例
    embedder = MarkdownEmbedder()
    
    print("開始嵌入 Markdown 文檔到 ChromaDB...")
    print(f"Schema 目錄: {schema_dir}")
    print(f"Examples 目錄: {examples_dir}")
    
    # 執行嵌入
    embedder.embed_documents(schema_dir, examples_dir)
    
    # 顯示集合信息
    info = embedder.get_collection_info()
    print(f"\n嵌入完成！")
    print(f"集合名稱: {info.get('collection_name', 'N/A')}")
    print(f"總文檔數: {info.get('total_documents', 'N/A')}")
    
    # 測試搜索
    test_search_function(embedder, "打擊率", 3)
    test_search_function(embedder, "全壘打", 2)
    test_search_function(embedder, "投球統計", 2)
    
if __name__ == "__main__":
    main()
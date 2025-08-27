import os
import chromadb
import pandas as pd
from chromadb import Documents, EmbeddingFunction, Embeddings
from google import genai
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '..', '..', '..', '.env')
load_dotenv(env_path)

client = genai.Client()

DOCUMENT1 = """
  操作氣候控制系統  您的 Googlecar 有一個氣候控制
  系統，允許您調節車內的溫度和氣流。
  要操作氣候控制系統，請使用位於
  中控台上的按鈕和旋鈕。  溫度：溫度旋鈕控制
  車內的溫度。順時針轉動旋鈕以提高
  溫度，或逆時針轉動以降低溫度。
  氣流：氣流旋鈕控制車內的氣流量。
  順時針轉動旋鈕以增加氣流，或逆時針轉動
  以減少氣流。風扇速度：風扇速度旋鈕控制
  風扇的速度。順時針轉動旋鈕以增加風扇速度，或
  逆時針轉動以降低風扇速度。
  模式：模式按鈕允許您選擇所需的模式。可用的
  模式有：自動：汽車將自動調節溫度和
  氣流以保持舒適的水平。
  冷卻：汽車將向車內吹送冷空氣。
  加熱：汽車將向車內吹送暖空氣。
  除霜：汽車將向擋風玻璃吹送暖空氣以除霜。
"""
DOCUMENT2 = """
  您的 Googlecar 有一個大型觸控螢幕顯示器，提供對
  各種功能的存取，包括導航、娛樂和氣候
  控制。要使用觸控螢幕顯示器，只需觸摸所需的圖示。
  例如，您可以觸摸\"導航\"圖示以獲取前往
  目的地的方向，或觸摸\"音樂\"圖示來播放您最喜愛的歌曲。
"""
DOCUMENT3 = """
  換檔 您的 Googlecar 有自動變速器。要
  換檔，只需將換檔桿移動到所需位置。
  停車：此位置用於停車時。車輪被鎖定
  且汽車無法移動。
  倒車：此位置用於倒車。
  空檔：此位置用於在紅燈或交通中停車時。
  汽車不在檔位中，除非您踩油門踏板，否則不會移動。
  前進：此位置用於向前行駛。
  低檔：此位置用於在雪地或其他滑溜條件下行駛。
"""

documents = [DOCUMENT1, DOCUMENT2, DOCUMENT3]

from google.genai import types

class GeminiEmbeddingFunction(EmbeddingFunction):
  def __call__(self, input: Documents) -> Embeddings:
    EMBEDDING_MODEL_ID = "gemini-embedding-001"  # @param ["gemini-embedding-001", "text-embedding-004"] {"allow-input": true, "isTemplate": true}
    title = "自訂查詢"
    response = client.models.embed_content(
        model=EMBEDDING_MODEL_ID,
        contents=input,
        config=types.EmbedContentConfig(
          task_type="RETRIEVAL_DOCUMENT",
          title=title
        )
    )

    return response.embeddings[0].values

def create_chroma_db(documents, name):
  chroma_client = chromadb.PersistentClient(path="./chroma_db")
  db = chroma_client.create_collection(
      name=name,
      embedding_function=GeminiEmbeddingFunction()
  )

  for i, d in enumerate(documents):
    db.add(
      documents=d,
      ids=str(i)
    )
  return db

db = create_chroma_db(documents, "google-car-db")

sample_data = db.get(include=['documents', 'embeddings'])

# df = pd.DataFrame({
#     "IDs": sample_data['ids'][:3],
#     "Documents": sample_data['documents'][:3],
#     "Embeddings": [str(emb)[:50] + "..." for emb in sample_data['embeddings'][:3]]  # 截斷嵌入
# })

def get_relevant_passage(query, db):
  passage = db.query(query_texts=[query], n_results=1)['documents'][0][0]
  return passage

passage = get_relevant_passage("觸控螢幕功能", db)

print()
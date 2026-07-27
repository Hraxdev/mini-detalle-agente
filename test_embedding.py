from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

try:
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vector = embeddings.embed_query("Hola mundo")

    print("✅ Embedding generado correctamente")
    print(f"Dimensión: {len(vector)}")

except Exception as e:
    print(e)
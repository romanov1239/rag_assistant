import os
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client_llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma = chromadb.PersistentClient(path="chroma_db")
ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small",
)
collection = chroma.get_collection("docs", embedding_function=ef)

SYSTEM_PROMPT = """Ты — ассистент, отвечающий на вопросы строго по контексту.
Если ответа в контексте нет — скажи об этом честно.
В конце ответа указывай источники в формате [source]."""


def retrieve(question: str, k: int = 4):
    res = collection.query(query_texts=[question], n_results=k)
    return list(zip(res["documents"][0], res["metadatas"][0]))


def answer(question: str) -> str:
    chunks = retrieve(question)
    context = "\n\n---\n\n".join(
        f"[{m['source']}]\n{doc}" for doc, m in chunks
    )

    response = client_llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Контекст:\n{context}\n\nВопрос: {question}"},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content
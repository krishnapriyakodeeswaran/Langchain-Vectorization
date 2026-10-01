from fastapi import FastAPI
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config import EMBED_MODEL, INDEX_DIR

app = FastAPI(title="PDF Vector Search")

# Must be the same embedding settings as ingest.py
embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

# Load the FAISS index that ingest.py saved
vectorstore = FAISS.load_local(
    INDEX_DIR, embeddings, allow_dangerous_deserialization=True
)


class QueryRequest(BaseModel):
    query: str
    top_k: int = 3


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/query")
def query(req: QueryRequest):
    # Direct similarity search: no LLM, no chain
    results = vectorstore.similarity_search_with_score(req.query, k=req.top_k)
    return [
        {
            "chunk_text": doc.page_content,
            "page_number": doc.metadata.get("page", 0) + 1,  # PyPDF pages start at 0
            "score": float(score),
        }
        for doc, score in results
    ]
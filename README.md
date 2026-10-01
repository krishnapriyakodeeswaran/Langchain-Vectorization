# PDF Vectorisation Pipeline (LangChain / LangGraph)

Assessment for Nestack Technologies.

**Live deployment:** https://krishnapriya-nestack-submission-1.onrender.com/docs

- No authentication is required.
- `GET /` returns a health check. Test the API with `POST /query` on the `/docs` page.
- Free hosting sleeps when idle, so the first request may take 30-60 seconds.

## Overview

1. **Ingestion (`ingest.py`)**: loads a PDF, splits it into chunks, embeds the chunks, and saves them to a FAISS index.
2. **Retrieval (`app.py`)**: a FastAPI server with a `POST /query` endpoint that runs `similarity_search_with_score()` directly on the vector store. There is no LLM and no QA chain. It returns raw chunks.

## Setup and run

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
python ingest.py --file data/sample.pdf
uvicorn app:app --reload
```

Then open http://127.0.0.1:8000/docs. To regenerate `results.json`, keep the server running and run `python run_queries.py` in a second terminal.

## API

`POST /query`

Request:
```json
{ "query": "How is the submission evaluated?", "top_k": 3 }
```

Response: an array of `{ chunk_text, page_number, score }`.

Example:
```bash
curl -X POST https://krishnapriya-nestack-submission-1.onrender.com/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How is the submission evaluated?", "top_k": 3}'
```

**Score:** FAISS returns an L2 distance, so a **lower score means a better match**.

## Component choices

| Stage | Choice | Why |
|---|---|---|
| Loader | `PyPDFLoader` | Lightweight, and keeps the page number in each document's metadata, which the response needs. |
| Splitter | `RecursiveCharacterTextSplitter` | Splits at paragraphs, then sentences, then words, so chunks stay coherent. |
| Chunk size / overlap | 1000 / 200 | About 250 tokens per chunk, a good size for a small embedding model. The 20% overlap keeps sentences at chunk boundaries retrievable. |
| Embeddings | `FastEmbedEmbeddings` (`BAAI/bge-small-en-v1.5`) | Free, runs locally with no API key, and uses little memory (no PyTorch), so it fits on a free host. |
| Vector store | `FAISS` | Fast and local. `save_local()` is its built-in persistence method. |

Ingestion and retrieval share the same settings through `config.py`, so the query is embedded with the same model used for ingestion.

## Ingestion Graph (LangGraph)

Nodes: `load` -> `split` -> `embed` -> `store`

```mermaid
graph TD;
        __start__([<p>__start__</p>]):::first
        load(load)
        split(split)
        embed(embed)
        store(store)
        __end__([<p>__end__</p>]):::last
        __start__ --> load;
        embed --> store;
        load --> split;
        split --> embed;
        store --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
```

Printed node list:
```
Graph nodes: ['__start__', 'load', 'split', 'embed', 'store', '__end__']
```

## Sample output

Query: "How is the submission evaluated?"

(paste 1 or 2 results from your new results.json here)

The full output for five queries is in `results.json`.

## Project structure

```
ingest.py        ingestion pipeline (LangGraph)
app.py           retrieval API (FastAPI)
config.py        shared settings
run_queries.py   generates results.json
results.json     sample query output
requirements.txt dependencies
data/sample.pdf  input PDF
```

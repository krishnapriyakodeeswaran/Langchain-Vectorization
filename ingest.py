import argparse
from typing import TypedDict

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS
from langgraph.graph import StateGraph, START, END

from config import EMBED_MODEL, INDEX_DIR, CHUNK_SIZE, CHUNK_OVERLAP

class State(TypedDict, total=False):
    file: str          # path of the PDF
    pages: list        # pages loaded from the PDF
    chunks: list       # small pieces of text
    vectorstore: object

embeddings = FastEmbedEmbeddings(model_name=EMBED_MODEL, cache_dir="models")
def load(state):
    pages = PyPDFLoader(state["file"]).load()
    print("Step 1 - loaded pages:", len(pages))
    return {"pages": pages}

def split(state):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(state["pages"])
    print("Step 2 - created chunks:", len(chunks))
    return {"chunks": chunks}

def embed(state):
    vectorstore = FAISS.from_documents(state["chunks"], embeddings)
    print("Step 3 - embeddings created")
    return {"vectorstore": vectorstore}

def store(state):
    state["vectorstore"].save_local(INDEX_DIR)
    print("Step 4 - saved to folder:", INDEX_DIR)
    return {}

workflow = StateGraph(State)
workflow.add_node("load", load)
workflow.add_node("split", split)
workflow.add_node("embed", embed)
workflow.add_node("store", store)

workflow.add_edge(START, "load")
workflow.add_edge("load", "split")
workflow.add_edge("split", "embed")
workflow.add_edge("embed", "store")
workflow.add_edge("store", END)

graph = workflow.compile()

parser = argparse.ArgumentParser()
parser.add_argument("--file", required=True, help="path to the PDF")
args = parser.parse_args()

print("Graph nodes:", list(graph.get_graph().nodes))
print(graph.get_graph().draw_mermaid())

graph.invoke({"file": args.file})
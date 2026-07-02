from fastapi import FastAPI, UploadFile, File
import tempfile
import shutil

from pdf_loader import extract_text_from_pdf
from chunking import chunk_text
from embeddings import embed_chunks_advanced

from qdrant_db import (
    create_collection,
    insert_chunks,
    search_context
)

from ollama_client import call_ollama

app = FastAPI(title="Research Paper RAG API")

create_collection()


@app.get("/")
def home():
    return {
        "message": "Research Paper RAG API is running."
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        shutil.copyfileobj(file.file, temp)
        pdf_path = temp.name

    pages = extract_text_from_pdf(pdf_path)

    chunks = chunk_text(
        pages,
        max_chunk_size=800
    )

    embedded_chunks = embed_chunks_advanced(chunks)

    insert_chunks(embedded_chunks)

    return {
        "status": "success",
        "pages": len(pages),
        "chunks": len(chunks),
        "vectors_indexed": len(embedded_chunks)
    }


@app.post("/ask")
async def ask(question: str):

    context = search_context(question)

    prompt = f"""
You are a research assistant.

Answer ONLY from the given context.

If the answer is not found in the context, reply:
"I couldn't find this information in the document."

Context:
{context}

Question:
{question}

Answer:
"""

    answer = call_ollama(prompt)

    return {
        "question": question,
        "answer": answer
    }

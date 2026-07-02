from fastapi import FastAPI, UploadFile, File
import tempfile
import shutil

from pdf_loader import extract_text_from_pdf
from chunking import chunk_text
from embeddings import embed_chunks_advanced

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Research RAG API Running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        shutil.copyfileobj(file.file, temp)
        pdf_path = temp.name

    # Pipeline
    pages = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(pages)
    embedded_chunks = embed_chunks_advanced(chunks)

    # Normally you'd insert into Qdrant here

    return {
        "pages": len(pages),
        "chunks": len(chunks),
        "embeddings_created": len(embedded_chunks)
    }

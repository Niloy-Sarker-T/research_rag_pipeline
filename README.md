# Research Paper RAG Assistant

A Retrieval-Augmented Generation (RAG) application for semantic question answering over research papers. The system extracts text from PDFs, generates semantic embeddings, stores them in Qdrant, and retrieves relevant context to generate answers using a local LLM through Ollama.

---

## Features

- 📄 PDF text extraction with page preservation
- ✂️ Section-aware text chunking
- 🧠 Semantic embeddings using `all-MiniLM-L6-v2`
- ⚡ Batch embedding generation
- 🔍 Vector search with Qdrant
- 🤖 Local LLM inference using Ollama
- 🌐 REST API built with FastAPI
- 📌 Metadata preservation (page number, section, chunk ID)

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| API | FastAPI |
| PDF Processing | pdfplumber |
| Embeddings | Sentence-Transformers (`all-MiniLM-L6-v2`) |
| Vector Database | Qdrant |
| LLM | Ollama (Llama 3/Mistral/Gemma) |
| Deep Learning | PyTorch |

---

## Project Structure

```text
research_rag/
│
├── main.py                # FastAPI application
├── pdf_loader.py          # PDF text extraction
├── chunking.py            # Intelligent chunking
├── embeddings.py          # Embedding generation
├── qdrant_db.py           # Vector database operations
├── ollama_client.py       # Ollama API client
└── requirements.txt
```

---

## Pipeline

```text
               OFFLINE

PDF
 │
 ▼
PDF Extraction
 │
 ▼
Section-aware Chunking
 │
 ▼
Sentence Embeddings
 │
 ▼
Qdrant Vector Store

────────────────────────────────────

                ONLINE

User Question
 │
 ▼
FastAPI
 │
 ▼
Question Embedding
 │
 ▼
Qdrant Similarity Search
 │
 ▼
Retrieve Top-k Chunks
 │
 ▼
Prompt Construction
 │
 ▼
Ollama
 │
 ▼
Generated Answer
```

---

## Core Components

### PDF Loader

- Extracts text page by page using `pdfplumber`
- Preserves page numbers for traceability

Output

```python
{
    "page_number": 1,
    "text": "..."
}
```

---

### Chunking

- Detects research paper sections using regex
- Splits text into ~800-character chunks
- Preserves metadata

Output

```python
{
    "chunk_id": 1,
    "section": "Introduction",
    "page_number": 2,
    "text": "..."
}
```

---

### Embeddings

- Uses `all-MiniLM-L6-v2`
- Produces 384-dimensional embeddings
- Supports configurable batch processing

Output

```python
{
    "chunk_id": 1,
    "section": "Introduction",
    "page_number": 2,
    "text": "...",
    "embedding": np.array(...)
}
```

---

### Qdrant

Stores:

- Embedding vectors
- Chunk text
- Page number
- Section
- Chunk metadata

Used for semantic similarity search during retrieval.

---

### Ollama

Receives the prompt containing:

- Retrieved context
- User question

Returns the generated answer using a locally running LLM.

---

## API Endpoints

### Upload PDF

```http
POST /upload
```

Processes the uploaded PDF through:

- Text extraction
- Chunking
- Embedding generation
- Vector indexing in Qdrant

---

### Ask Question

```http
POST /ask
```

Workflow:

1. Embed user query
2. Retrieve relevant chunks from Qdrant
3. Construct prompt
4. Send prompt to Ollama
5. Return generated answer

---

## Design Principles

- **Separation of Concerns** – Each module has a single responsibility.
- **Pipeline Architecture** – Data flows through extraction, chunking, embedding, retrieval, and generation.
- **Batch Processing** – Efficient embedding generation.
- **Metadata Preservation** – Page number, section, and chunk ID remain available throughout the pipeline.
- **Modular Design** – Components such as the embedding model, vector database, or LLM can be replaced independently.

---

## Installation

```bash
pip install -r requirements.txt
```

Run Qdrant:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Run Ollama:

```bash
ollama serve
ollama pull llama3
```

Start the API:

```bash
uvicorn main:app --reload
```

Interactive API documentation:

```
http://localhost:8000/docs
```

---

## Future Improvements

- Multi-PDF indexing
- Hybrid retrieval (BM25 + Vector Search)
- Cross-encoder reranking
- OCR support for scanned PDFs
- Figure and table retrieval
- Citation-aware answers
- Streaming responses

---

## License

MIT

# Multiple PDF Research Assistant RAG Application

A sophisticated Retrieval-Augmented Generation (RAG) system designed for intelligent research paper analysis and question-answering across multiple PDF documents.

---

## Overview

This application is built to extract, process, and intelligently retrieve information from multiple research papers using semantic embeddings and advanced text chunking. It enables researchers to query across multiple PDF documents and get contextually relevant answers powered by embeddings-based retrieval.

---

## Technology Stack

### Core Libraries

| Technology | Version | Purpose |
|---|---|---|
| **Python** | 3.8+ | Programming language |
| **PyTorch (torch)** | Latest | Deep learning framework for embeddings and models |
| **pdfplumber** | Latest | PDF text extraction and parsing |
| **sentence-transformers** | Latest | Semantic embeddings generation |
| **NumPy** | Latest | Numerical computation and array operations |

### Key Models & Services

- **Embedding Model**: `all-MiniLM-L6-v2` (Sentence Transformers)
  - Lightweight, fast, and efficient embeddings
  - 384-dimensional vectors
  - Suitable for similarity search and semantic retrieval
  
---

## Architecture

### Project Structure

```
research_rag/
├── core/
│   ├── pdf_loader.py      # PDF extraction module
│   ├── chunking.py        # Text chunking with section detection
│   ├── embeddings.py      # Semantic embedding generation
│   └── dummy.py           # GPU configuration test
└── core_backup/
    └── pdf_loader.py      # Backup of PDF loader
```

---

## Core Components

### 1. **PDF Loader** (`pdf_loader.py`)

**Functionality**: Extracts text from PDF documents page-by-page.

**Features**:
- Page-level text extraction using `pdfplumber`
- Preserve page numbering for document tracking
- Handles multiple PDF files
- Returns structured data with page metadata

**Input**: PDF file path  
**Output**: List of dictionaries containing `page_number` and `text`

```python
{
    "page_number": 1,
    "text": "extracted text content..."
}
```

### 2. **Text Chunking** (`chunking.py`)

**Functionality**: Intelligently segments extracted text into manageable chunks with section awareness.

**Features**:
- **Section Detection**: Automatically identifies research paper sections
  - Abstract, Introduction, Method, Results, Discussion, Conclusion
- **Configurable Chunk Size**: Default 800 characters per chunk
- **Metadata Preservation**:
  - Chunk ID
  - Section name
  - Page number
  - Text content
- **Boundary-Aware Chunking**: Respects section boundaries

**Input**: List of page dictionaries  
**Output**: List of chunk objects with metadata

```python
{
    "chunk_id": 1,
    "section": "Introduction",
    "page_number": 2,
    "text": "chunk text..."
}
```

### 3. **Embeddings Generation** (`embeddings.py`)

**Functionality**: Generates semantic embeddings for chunked text using pre-trained transformer models.

**Features**:
- **Batch Processing**: Efficiently handles large datasets
  - Configurable batch size (default: 32)
  - Progress tracking during encoding
- **Model**: Sentence Transformers (`all-MiniLM-L6-v2`)
- **GPU Control**: CPU-only mode for compatibility
  - Disabled via `CUDA_VISIBLE_DEVICES = "-1"`
- **Vector Output**: NumPy arrays (384-dimensional)
- **Metadata Attachment**: Preserves chunk metadata with embeddings

**Input**: List of chunk dictionaries  
**Output**: List of embedded chunks with full metadata

```python
{
    "chunk_id": 1,
    "section": "Introduction",
    "page_number": 2,
    "text": "chunk text...",
    "embedding": np.array([...])  # 384-dimensional vector
}
```

---

## Data Flow Pipeline

```
PDF Files
    ↓
[PDF Loader]
    ↓
Pages with Text
    ↓
[Text Chunking]
    ↓
Chunks with Metadata & Section
    ↓
[Embeddings Generation]
    ↓
Semantic Vector Embeddings
    ↓
Vector Database / Retrieval System
    ↓
Query Processing & RAG
```

---

## Key Features

### ✨ Section-Aware Processing
- Automatically detects standard research paper sections
- Groups related content together
- Preserves document structure

### ⚡ Batch Processing
- Efficient embedding generation for large datasets
- Configurable batch sizes for memory optimization
- Progress tracking during processing

### 📄 Document Tracking
- Page numbers preserved throughout pipeline
- Source attribution for retrieved chunks
- Full auditability of retrieved information

### 🔍 Semantic Retrieval Ready
- Embeddings enable similarity-based search
- Support for various embedding-based retrieval methods
- Compatible with vector databases (Pinecone, Weaviate, Chroma, etc.)

---

## Installation & Setup

### Prerequisites
```bash
python >= 3.8
pip
```

### Install Dependencies
```bash
pip install pdfplumber sentence-transformers torch numpy
```

### Optional: Requirements File
Create a `requirements.txt` file:
```
pdfplumber>=0.9.0
sentence-transformers>=2.2.0
torch>=1.9.0
numpy>=1.21.0
```

Install from requirements:
```bash
pip install -r requirements.txt
```

---

## Usage Example

```python
from core.pdf_loader import extract_text_from_pdf
from core.chunking import chunk_text
from core.embeddings import embed_chunks_advanced

# Step 1: Extract text from PDF
pages = extract_text_from_pdf("path/to/research_paper.pdf")
print(f"Extracted {len(pages)} pages")

# Step 2: Chunk the text
chunks = chunk_text(pages, max_chunk_size=800)
print(f"Created {len(chunks)} chunks")

# Step 3: Generate embeddings
embedded_chunks = embed_chunks_advanced(chunks, batch_size=32)
print(f"Generated embeddings for {len(embedded_chunks)} chunks")

# Step 4: Store in vector database and enable retrieval
# (Integrated with qdrant)
```

---

## Configuration Options

### Chunking Configuration
| Parameter | Default | Purpose |
|---|---|---|
| `max_chunk_size` | 800 | Maximum characters per chunk |
| Section Pattern | Regex | Detects: Abstract, Introduction, Method, Results, Discussion, Conclusion |

### Embedding Configuration
| Parameter | Default | Purpose |
|---|---|---|
| `batch_size` | 32 | Chunks processed per batch |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence transformers model |
| `CUDA_VISIBLE_DEVICES` | `-1` | Disables GPU, uses CPU |

---




---

## Performance Considerations

### Optimization Tips
1. **Batch Size**: Adjust based on available RAM
   - Larger batches = faster but more memory
   - Smaller batches = slower but lower memory

2. **Model Selection**: `all-MiniLM-L6-v2` is optimized for:
   - Fast inference
   - Low memory footprint
   - Reasonable semantic quality

3. **GPU Usage**: 
   - Currently configured for CPU-only
   - Enable GPU by removing `CUDA_VISIBLE_DEVICES = "-1"` for faster processing

### Scalability
- Supports multiple PDF files
- Handles large documents through chunking
- Batch processing prevents memory overflow

---



---

## License

Specify your license here (MIT, Apache 2.0, etc.)

---

## Contact & Contribution

For questions, issues, or contributions, please refer to the project repository.

---

**Last Updated**: March 2026  
**Version**: 1.0.0

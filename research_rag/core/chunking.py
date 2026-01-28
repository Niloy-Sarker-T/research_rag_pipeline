import re
from typing import List, Dict

def chunk_text(pages: List[Dict], max_chunk_size: int = 800) -> List[Dict]:
    chunks = []
    current_chunk = ""
    current_section = "Unknown"
    chunk_id = 1

    section_pattern = re.compile(r"(?i)(abstract|introduction|method|results|discussion|conclusion)")

    for page in pages:
        page_number = page["page_number"]
        text = page["text"]

        for line in text.split("\n"):
            if section_pattern.search(line.strip()):
                if current_chunk.strip():
                    chunks.append({
                        "chunk_id": chunk_id,
                        "section": current_section,
                        "page_number": page_number,  # <--- add this
                        "text": current_chunk.strip()
                    })
                    chunk_id += 1
                    current_chunk = ""
                current_section = line.strip()
            else:
                current_chunk += " " + line.strip()

            if len(current_chunk) > max_chunk_size:
                chunks.append({
                    "chunk_id": chunk_id,
                    "section": current_section,
                    "page_number": page_number,  # <--- add this
                    "text": current_chunk.strip()
                })
                chunk_id += 1
                current_chunk = ""

    if current_chunk.strip():
        chunks.append({
            "chunk_id": chunk_id,
            "section": current_section,
            "page_number": page_number,  # <--- add this
            "text": current_chunk.strip()
        })

    return chunks





from pdf_loader import extract_text_from_pdf


pages = extract_text_from_pdf(r"E:\ishmambhai\research_rag\venv\paper_1.pdf")
print(f"Extracted {len(pages)} pages from PDF.")

# Step 2: Chunk the text
chunks = chunk_text(pages, max_chunk_size=800)
print(f"Total chunks generated: {len(chunks)}\n")

# Step 3: Inspect the first few chunks
for chunk in chunks[:5]:
    print(f"Chunk ID: {chunk['chunk_id']}")
    print(f"Section: {chunk['section']}")
    print(f"Page: {chunk['page_number']}")
    print(f"Text (first 200 chars): {chunk['text'][:200]}")
    print("-"*50)
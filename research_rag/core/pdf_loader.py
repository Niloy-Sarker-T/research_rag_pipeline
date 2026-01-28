import pdfplumber

def extract_text_from_pdf(pdf_path):
    full_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                full_text.append({"page_number": i+1, "text": text})
    return full_text



pages = extract_text_from_pdf(r"E:\ishmambhai\research_rag\venv\paper_1.pdf")

print(f"Extracted {len(pages)} pages.")
print(pages[0])

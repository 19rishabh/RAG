from pathlib import Path
from typing import List, Dict
from PyPDF2 import PdfReader
from docx import Document

def load_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def load_pdf(path: Path) -> str:
    text = []
    with open(path, "rb") as f:
        reader = PdfReader(f)
        for p in reader.pages:
            text.append(p.extract_text() or "")
    return "\n".join(text)

def load_docx(path: Path) -> str:
    doc = Document(path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)

# main function to load documents from a directory
def load_documents(doc_dir: str) -> List[Dict]:
    doc_dir = Path(doc_dir)
    docs = []
    for p in doc_dir.glob("**/*"):
        if p.suffix.lower() in [".pdf"]:
            text = load_pdf(p)
        elif p.suffix.lower() in [".txt", ".md"]:
            text = load_txt(p)
        elif p.suffix.lower() in [".docx"]:
            text = load_docx(p)
        else:
            continue
        if text.strip():
            docs.append({"id": str(p.relative_to(doc_dir)), "text": text, "source": str(p)})
    return docs

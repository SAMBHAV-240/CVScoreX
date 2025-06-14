import os
import docx2txt
import fitz  # PyMuPDF

def extract_text_from_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext == ".docx":
        return docx2txt.process(filepath)

    elif ext == ".pdf":
        text = ""
        with fitz.open(filepath) as doc:
            for page in doc:
                text += page.get_text()
        return text

    elif ext == ".txt":
        with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
            return file.read()

    else:
        return "Unsupported file format. Please upload a PDF, DOCX, or TXT file."

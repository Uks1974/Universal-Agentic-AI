import pandas as pd
import pdfplumber
from docx import Document
from pptx import Presentation
from PIL import Image
import pytesseract

def parse_file(path, file_type):
    if file_type == "excel":
        return pd.read_excel(path)

    if file_type == "pdf":
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    if file_type == "word":
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)

    if file_type == "ppt":
        prs = Presentation(path)
        return "\n".join(
            shape.text for slide in prs.slides
            for shape in slide.shapes if hasattr(shape, "text")
        )

    if file_type == "image":
        img = Image.open(path)
        return pytesseract.image_to_string(img)
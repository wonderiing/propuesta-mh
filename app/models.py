import fitz  # PyMuPDF
import docx

def extract_text_from_pdf(file_path):
    """Extrae el texto de un archivo PDF."""
    doc = fitz.open(file_path)
    text = "\n".join([page.get_text() for page in doc])
    return text

def extract_text_from_docx(file_path):
    """Extrae el texto de un archivo DOCX."""
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

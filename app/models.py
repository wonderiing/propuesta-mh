import fitz  # PyMuPDF
import docx

from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class CV(Base):
    __tablename__ = "cvs"

    id = Column(Integer, primary_key=True, index=True)
    cv = Column(Text, nullable=False)
    job_desc = Column(Text, nullable=False)



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

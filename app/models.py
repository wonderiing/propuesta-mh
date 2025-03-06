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
    """Extrae el texto de un archivo PDF de manera optimizada."""
    try:
        doc = fitz.open(file_path)
        text = "".join(page.get_text() for page in doc)
        doc.close()  
        return text
    except Exception as e:
        return f"Error: {str(e)}"

def extract_text_from_docx(file_path):
    """Extrae el texto de un archivo DOCX de manera optimizada."""
    try:
        doc = docx.Document(file_path)
        paragraphs = []
        paragraphs_append = paragraphs.append  
        
        for para in doc.paragraphs:
            paragraphs_append(para.text)
            
        return "\n".join(paragraphs)
    except Exception as e:
        return f"Error: {str(e)}"

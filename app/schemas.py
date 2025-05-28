from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FeedbackRequest(BaseModel):
    candidato: str
    comentario: str

class CV(Base):
    __tablename__ = "cvs"

    id = Column(Integer, primary_key=True, index=True)
    cv = Column(Text, nullable=False)
    job_desc = Column(Text, nullable=False)

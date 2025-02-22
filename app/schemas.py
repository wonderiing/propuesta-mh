from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    candidato: str
    comentario: str

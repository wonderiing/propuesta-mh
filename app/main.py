from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware

from app.services import process_cv
from app.models import extract_text_from_pdf, extract_text_from_docx
from app.schemas import FeedbackRequest

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.post("/procesar-cv/")
async def procesar_cv(
    file: UploadFile = File(...),
    job_description: str = Body(...),  
):
    return await process_cv(file, job_description)

@app.post("/feedback/")
async def recibir_feedback(feedback: FeedbackRequest):
    return {"mensaje": f"Feedback recibido para {feedback.candidato}: {feedback.comentario}"}

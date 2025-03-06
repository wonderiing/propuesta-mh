import ollama
import os
import asyncio
from tempfile import NamedTemporaryFile
from concurrent.futures import ThreadPoolExecutor
from app.models import extract_text_from_pdf, extract_text_from_docx
from app.database import SessionLocal
from app.models import CV

executor = ThreadPoolExecutor(max_workers=5)

PROMPT_TEMPLATE = """
Analiza el CV del candidato y evalúa su adecuación para el puesto basado en la descripción del trabajo:

Descripción del trabajo y área requerida:
{job_description}

CV del candidato:
{cv_text}

Devuelve solo lo siguiente en español:

- Calificación del candidato de 1 a 10, de acuerdo con las siguientes directrices:
    - **1-3**: El candidato no cumple con los requisitos básicos del puesto. No tiene experiencia clave o habilidades fundamentales necesarias para el puesto.
    - **4-5**: El candidato tiene algunas habilidades relevantes, pero le faltan conocimientos o experiencia en áreas esenciales del puesto.
    - **6-7**: El candidato tiene experiencia en algunas áreas clave, pero le falta habilidad o experiencia en otros aspectos cruciales del puesto.
    - **8-9**: El candidato cumple con la mayoría de los requisitos del puesto, aunque podría necesitar capacitación adicional en áreas específicas.
    - **10**: El candidato cumple completamente con todos los requisitos del puesto y tiene la experiencia adecuada para desempeñarse con éxito.

- **Si el candidato no es adecuado para el puesto y tiene calificación baja**:
  - Menciona **2 áreas clave** que el candidato necesita mejorar para cumplir con los requisitos del puesto. Estas áreas deben estar directamente relacionadas con las habilidades y experiencias clave necesarias para el puesto.

- **Si el candidato es adecuado para el puesto y tiene una calificación decente**:
  - Proporciona **3 razones claras y específicas** por las que el candidato es adecuado para el puesto, basadas en los requisitos detallados en la descripción del trabajo.

Nota: Sé **estricto** en la evaluación. Asegúrate de que la evaluación se base principalmente en la relevancia de las habilidades específicas del puesto. Si el candidato no cumple con los requisitos esenciales, **no menciones las razones de adecuación** y otorga una calificación baja.
"""

async def save_cv_to_db(texto: str, job_description: str):
    """Guarda el CV en la base de datos de forma asíncrona"""
    def _save_to_db():
        db = SessionLocal()
        try:
            nuevo_cv = CV(cv=texto, job_desc=job_description)
            db.add(nuevo_cv)
            db.commit()
            db.refresh(nuevo_cv)
            return nuevo_cv
        finally:
            db.close()
            
    return await asyncio.to_thread(_save_to_db)

def extract_text(file_path, file_ext):
    """Extrae texto de archivos en un thread separado"""
    if file_ext == "pdf":
        return extract_text_from_pdf(file_path)
    elif file_ext == "docx":
        return extract_text_from_docx(file_path)
    return ""

async def query_ollama(cv_text, job_description):
    """Consulta al modelo Ollama de manera asíncrona"""
    prompt = PROMPT_TEMPLATE.format(job_description=job_description, cv_text=cv_text)
    return await asyncio.to_thread(
        lambda: ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": prompt}])
    )

async def process_cv(file, job_description):
    """Procesa el CV de manera optimizada y asíncrona."""
    file_ext = file.filename.split(".")[-1].lower()
    
    if file_ext not in ["pdf", "docx"]:
        return {"error": "Formato no soportado"}
    
    with NamedTemporaryFile(suffix=f".{file_ext}", delete=False) as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name
    
    try:
        text = await asyncio.to_thread(extract_text, temp_file_path, file_ext)
        
        ollama_task = query_ollama(text, job_description)
        db_task = save_cv_to_db(text, job_description)
                response, _ = await asyncio.gather(ollama_task, db_task)
        
        evaluacion = response["message"]["content"]
        return {"evaluacion": evaluacion}
    
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

import ollama
import os
from app.models import extract_text_from_pdf, extract_text_from_docx

async def process_cv(file, job_description):
    """Procesa el CV, extrayendo texto y enviando la solicitud a Ollama."""
    file_ext = file.filename.split(".")[-1]
    
    # Guardamos el archivo temporalmente
    file_path = f"./temp.{file_ext}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extraemos el texto del archivo
    text = ""
    if file_ext == "pdf":
        text = extract_text_from_pdf(file_path)
    elif file_ext == "docx":
        text = extract_text_from_docx(file_path)
    else:
        os.remove(file_path)  # Limpieza en caso de formato no soportado
        return {"error": "Formato no soportado"}

    # Creamos el prompt para Ollama
    prompt = f"""
    Analiza este CV y dime qué tan adecuado es el candidato para el puesto basado en esta descripción del trabajo:
    
    Descripción del trabajo:    
    {job_description}
    
    CV del candidato:
    {text}

    
    Devuelve una evaluación detallada en español, incluyendo:
    - ¿Cuánto se ajusta la experiencia del candidato a las habilidades requeridas para el puesto ?
    - ¿Qué habilidades necesita mejorar para calificar completamente para este puesto?
    - Proporciona una calificación del 1 al 10 basada en la adecuación al puesto.   
      """
    
    # Interacción con el modelo Ollama
    response = ollama.chat(model="qwen2.5:3b", messages=[{"role": "user", "content": prompt}])
    
    # Limpiamos el archivo temporal
    os.remove(file_path)

    return {"evaluacion": response["message"]["content"]}

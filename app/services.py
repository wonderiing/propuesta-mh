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
    Analiza el CV del candidato y evalúa su adecuación para el puesto basado en la descripción del trabajo:

    Descripción del trabajo y área requerida:
    {job_description}

    CV del candidato:
    {text}

    Devuelve solo lo siguiente en español:

    - Calificación del candidato de 1 a 10, de acuerdo con las siguientes directrices:
        - **1-3**: El candidato no cumple con los requisitos básicos del puesto. No tiene experiencia clave o habilidades fundamentales necesarias para el puesto.
        - **4-5**: El candidato tiene algunas habilidades relevantes, pero le faltan conocimientos o experiencia en áreas esenciales del puesto.
        - **6-7**: El candidato tiene experiencia en algunas áreas clave, pero le falta habilidad o experiencia en otros aspectos cruciales del puesto.
        - **8-9**: El candidato cumple con la mayoría de los requisitos del puesto, aunque podría necesitar capacitación adicional en áreas específicas.
        - **10**: El candidato cumple completamente con todos los requisitos del puesto y tiene la experiencia adecuada para desempeñarse con éxito.

    - **Si el candidato no es adecuado para el puesto y tiene calificacion baja**:
    - Menciona **2 áreas clave** que el candidato necesita mejorar para cumplir con los requisitos del puesto. Estas áreas deben estar directamente relacionadas con las habilidades y experiencias clave necesarias para el puesto.

    - **Si el candidato es adecuado para el puest y tiene una calificacion decente**:
    - Proporciona **3 razones claras y específicas** por las que el candidato es adecuado para el puesto, basadas en los requisitos detallados en la descripción del trabajo.

    Nota: Sé **estricto** en la evaluación. Asegúrate de que la evaluación se base principalmente en la relevancia de las habilidades específicas del puesto. Si el candidato no cumple con los requisitos esenciales, **no menciones las razones de adecuación** y otorga una calificación baja.
    """
        
    # Interacción con el modelo Ollama
    response = ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": prompt}])
    
    # Limpiamos el archivo temporal
    os.remove(file_path)

    return {"evaluacion": response["message"]["content"]}

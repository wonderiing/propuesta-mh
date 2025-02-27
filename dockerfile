# Imagen base de Python
FROM python:3.11

# Instalar dependencias necesarias para Ollama
RUN apt update && apt install -y curl

# Instalar Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Descargar el modelo de IA que usará la API
RUN ollama pull llama3.2:3b

# Crear y definir el directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto de la API
EXPOSE 8000

# Comando para iniciar PostgreSQL y la API
CMD ["sh", "-c", "ollama serve & alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

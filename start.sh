#!/bin/bash

# Descargar e instalar Ollama (para Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Iniciar Ollama en segundo plano
ollama serve &

# Esperar unos segundos para asegurar que Ollama está en ejecución
sleep 5

# Descargar el modelo que necesitas
ollama pull llama3.2:3b

# Ejecutar migraciones de base de datos
alembic upgrade head  # O python manage.py migrate si usas Django

# Iniciar la aplicación (FastAPI con Uvicorn)
uvicorn app.main:app --host 0.0.0.0 --port 8000

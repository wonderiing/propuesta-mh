# API de Filtrado de Candidatos

Esta API de FastAPI permite filtrar candidatos basándose en una descripción de puesto (`job_description`) y un currículum vitae (`CV`) en formato PDF o DOCX. Retorna una calificación y feedback inicial, diseñada para ser utilizada en las etapas tempranas del proceso de selección.

## Características

* **Entrada Flexible:** Acepta descripciones de puesto en texto y CVs en PDF o DOCX.
* **Calificación de Candidatos:** Proporciona una puntuación que indica la relevancia del candidato para el puesto.
* **Feedback Inicial:** Ofrece comentarios concisos para orientar la decisión.
* **Tecnología Ollama:** Aprovecha modelos de lenguaje locales para el procesamiento inteligente de texto.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes componentes:

* **Python 3.9+**
* **Ollama:** Necesitas instalar Ollama y tener un modelo de lenguaje descargado y en ejecución. Se recomienda `llama2` o `mistral` para comenzar.

    * **Instalación de Ollama:** Sigue las instrucciones en la página oficial de Ollama: [https://ollama.ai/download](https://ollama.ai/download)
    * **Descargar un modelo (ej. Llama 2):** Abre tu terminal y ejecuta:
        ```bash
        ollama run llama2
        ```
        Esto descargará el modelo si no lo tienes y lo iniciará. Asegúrate de que el modelo esté en ejecución cuando inicies la API.

## Instalación y Configuración del Proyecto

Sigue estos pasos para poner en marcha el proyecto:

1.  **Clonar el Repositorio:**
    ```bash
    git clone <URL_DEL_TU_REPOSITORIO>
    cd <nombre_del_directorio_del_repositorio>
    ```

2.  **Crear y Activar un Entorno Virtual:**
    Es
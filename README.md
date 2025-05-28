# Candidate Filtering API

This FastAPI application offers an API to filter job candidates based on a `job_description` and a `CV` provided as a PDF or DOCX file. It returns a **score** and initial **feedback**, designed for early-stage candidate screening.

## Features

* **Flexible Input:** Accepts job descriptions as plain text and CVs in PDF or DOCX formats.
* **Candidate Scoring:** Provides a relevancy score indicating how well a candidate matches the job.
* **Initial Feedback:** Offers concise comments to guide your hiring decisions.
* **Ollama Integration:** Leverages local language models via Ollama for intelligent text processing.

---

## Prerequisites

Before setting up the project, ensure you have the following installed:

* **Python 3.9+**
* **Ollama:** You need Ollama installed and a language model downloaded and running. `llama2` or `mistral` are good starting points.

    * **Install Ollama:** Follow the instructions on the official Ollama website: [https://ollama.ai/download](https://ollama.ai/download)
    * **Download a Model (e.g., Llama 2):** Open your terminal and run:
        ```bash
        ollama run llama2
        ```
        This command will download the model if you don't have it and then start it. **Ensure your chosen model is running when you launch the API.**

---

## Installation and Project Setup

Follow these steps to get the project up and running:

1.  **Clone the Repository:**
    ```bash
    git clone <YOUR_REPOSITORY_URL>
    cd <your_repository_directory_name>
    ```

2.  **Create and Activate a Virtual Environment:**
    It's best practice to use a virtual environment to manage project dependencies.

    ```bash
    python -m venv venv
    ```

    * **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

3.  **Install Dependencies:**
    With your virtual environment activated, install all required project dependencies from `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

    If you don't have a `requirements.txt` file yet, you'll need to create one with your dependencies. A common set for this type of project might include:

    ```
    fastapi
    uvicorn
    python-multipart
    pydantic
    ollama # Or a client library for Ollama, if available/necessary
    python-docx
    pypdf
    ```
    *Note: The exact Ollama integration might require a specific client library or direct HTTP calls. Adjust `ollama` dependency as needed based on your implementation.*

---

## Running the API

Once you've completed the setup, you can run the FastAPI application:

1.  **Ensure Ollama is Running:** Double-check that your chosen Ollama model (e.g., `llama2`) is active in your terminal. You can start it with `ollama run llama2`.

2.  **Start the FastAPI Server:**
    ```bash
    uvicorn main:app --reload
    ```
    * Replace `main:app` with the actual name of your Python file and FastAPI app instance if they are different (e.g., `my_api_file:my_fastapi_app`).
    * The `--reload` flag is useful during development as it automatically restarts the server on code changes.

3.  **Access the API Documentation:**
    Once the server is running, open your web browser and navigate to:
    ```
    [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    ```
    Here you will find the interactive API documentation (Swagger UI), allowing you to test the endpoints directly.

---

## API Endpoints

### `POST /filter-candidate/`

This endpoint processes a job description and a candidate's CV to provide a compatibility score and feedback.

* **Request Body:** `multipart/form-data`
    * `job_description` (string): The text describing the job requirements.
    * `cv_file` (file): The candidate's CV in PDF or DOCX format.

* **Responses:**
    * `200 OK`: Successful processing.
        ```json
        {
          "score": 85,
          "feedback": "Strong match with relevant experience in AI and machine learning. Lacks specific project examples mentioned in the job description."
        }
        ```
    * `400 Bad Request`: Invalid input (e.g., missing file, unsupported file type).
    * `500 Internal Server Error`: An error occurred during processing (e.g., Ollama model not running, internal processing issue).

---

## Project Structure (Example)
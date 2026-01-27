# eCOMET Chatbot Backend

This directory contains the FastAPI backend for the eCOMET chatbot.

## Setup

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Set your Gemini API Key:
    ```bash
    export GEMINI_API_KEY=your_key_here
    ```
3.  Run the server:
    ```bash
    uvicorn main:app --reload
    ```

## Endpoints

-   `POST /chat`: Accepts JSON `{"message": "user query"}` and returns `{"response": "bot answer"}`.
-   `GET /health`: Health check.

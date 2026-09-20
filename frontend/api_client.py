import os

import requests
from dotenv import load_dotenv


load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)


def upload_pdf(file):
    response = requests.post(
        f"{BACKEND_URL}/upload",
        files={
            "file": (
                file.name,
                file.getvalue(),
                "application/pdf"
            )
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()


def ask_studymate(question, document_id):
    response = requests.post(
        f"{BACKEND_URL}/query",
        json={
            "question": question,
            "document_id": document_id
        },
        timeout=180
    )

    response.raise_for_status()

    return response.json()


def summarize_document(document_id):
    response = requests.post(
        f"{BACKEND_URL}/summarize",
        json={
            "document_id": document_id
        },
        timeout=600
    )

    response.raise_for_status()

    return response.json()
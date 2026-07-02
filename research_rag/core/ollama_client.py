import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "llama3"     


def call_ollama(prompt):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload
    )

    response.raise_for_status()

    return response.json()["response"]

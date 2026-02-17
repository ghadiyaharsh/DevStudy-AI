import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3",
        "prompt": "Explain polymorphism in simple terms.",
        "stream": False
    }
)

print(response.json()["response"])
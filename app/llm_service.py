import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

def generate_response(prompt:str) -> str:
    
    system_prompt = """
You are DevStudy AI, a helpful assistant for students and developers.
Give clear, structured and concise answers.
"""

    final_prompt = system_prompt + "\nUser Question:\n" + prompt

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model":MODEL_NAME,
                "prompt": final_prompt,
                "stream":False
            }
        )
        
        data = response.json()
        return data.get("response","No response from model.")    
        
    except Exception as e:
        return f"Error:{str(e)}"
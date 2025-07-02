# callollama.py

import requests
import json

def callOLLAMA(user_message):
    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "phi3",  # Replace with the model you're using
            "prompt": user_message,
            "stream": False
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)

        if response.status_code == 200:
            data = response.json()
            return data.get("response", "Sorry, I didn't understand that.").strip()
        else:
            return f"Error: Unable to fetch response from OLLAMA. Status Code: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

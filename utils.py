import requests
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

HF_TOKEN = os.getenv("HF_TOKEN")
HF_API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def ask_huggingface(user_message):
    payload = {
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "messages": [
            {"role": "system", "content": """You are a helpful assistant for our education portal..."""},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }
    try:
        response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload, timeout=30)
        if response.status_code == 401:
            return "Invalid HF token."
        if response.status_code == 503:
            return "Model is loading. Please wait."
        if response.status_code == 429:
            return "Too many requests."
        if response.status_code != 200:
            return f"API error: HTTP {response.status_code}"
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "Request timed out."
    except Exception as e:
        return f"Error: {str(e)}"
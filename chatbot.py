import gradio as gr
import requests
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de la API
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

def llama_chat(prompt):
    if not API_URL or not API_KEY:
        return "Error: API_URL o API_KEY no están configurados correctamente."
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/llama-3-2-90b-vision-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('choices', [{}])[0].get('message', {}).get('content', "Sin respuesta")
    else:
        return f"Error: {response.status_code} - {response.text}"

# Configurar Gradio
def chatbot_interface(user_input):
    return llama_chat(user_input)

# Crear la interfaz de Gradio
iface = gr.Interface(
    fn=chatbot_interface,
    inputs=gr.Textbox(lines=2, placeholder="Escribe tu mensaje aquí..."),
    outputs=gr.Textbox(label="Respuesta del Chatbot"),
    title="Chatbot con Llama",
    description="Prueba rápida de chatbot usando AI/ML API."
)

# Iniciar la aplicación
if __name__ == "__main__":
    iface.launch()
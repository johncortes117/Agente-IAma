import gradio as gr
from fastapi import FastAPI
import requests
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de la API
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

def llama_chat(prompt):
    if not API_URL or not API_KEY:
        return "Error: API_URL o API_KEY no están configurados correctamente."
    
    # Configurar encabezados
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Sistema prompt mejorado para personalización
    system_prompt = """Eres un agente de inteligencia artificial que ayuda a los estudiantes a descubrir qué carrera universitaria pueden seguir. 
    Cuando el estudiante se presenta con su información personal, usa esos datos para personalizar tus recomendaciones según su edad y país.
    Pregunta sobre sus materias favoritas, rendimiento académico, intereses y metas profesionales.
    Siempre que hagas preguntas, preséntalas en una lista numerada y sé breve y directo."""
    
    payload = {
        "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return content.strip()
        else:
            return f"Error en la solicitud: {response.status_code}"
                
    except requests.exceptions.RequestException as e:
        return f"Error de conexión: {str(e)}"

# Configurar Gradio
def chatbot_interface(user_input):
    if not user_input.strip():
        return "Por favor, escribe un mensaje."
    return llama_chat(user_input)

# Crear la interfaz de Gradio
iface = gr.Interface(
    fn=chatbot_interface,
    inputs=gr.Textbox(
        lines=2, 
        placeholder="Cuéntame sobre tus intereses y materias favoritas..."
    ),
    outputs=gr.Textbox(label="Agente IAma"),
    title="🦙 Agente IAma - Tu Guía Vocacional",
    description="Estoy aquí para ayudarte a descubrir tu vocación profesional.",
    theme="soft",
    css=".gradio-container {background-color: #0a0a0a; min-height: 100vh;}"
)

# Crear la app FastAPI y configurar CORS
chatbot_app = FastAPI()
chatbot_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar Gradio en FastAPI
chatbot_app = gr.mount_gradio_app(chatbot_app, iface, path="/")
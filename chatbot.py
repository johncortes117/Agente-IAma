import gradio as gr
import requests
from dotenv import load_dotenv
import os
import json

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
    
    # Cuerpo de la solicitud según la documentación de la API
    payload = {
        "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        "messages": [
            {"role": "system", "content": "Eres un asistente útil."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000,  # Aumentado para permitir respuestas más largas
        "temperature": 0.7,
        "top_p": 1.0
    }
    
    try:
        # Hacer la solicitud POST
        response = requests.post(API_URL, headers=headers, json=payload)
        
        # Verificar si la respuesta es exitosa
        if response.status_code == 200:
            data = response.json()
            try:
                # Extraer solo el contenido del mensaje del asistente
                content = data["choices"][0]["message"]["content"]
                return content.strip()
            except (KeyError, IndexError) as e:
                return f"Error al procesar la respuesta: No se pudo extraer el contenido del mensaje"
        else:
            # Intentar parsear el mensaje de error
            try:
                error_data = response.json()
                if isinstance(error_data, dict) and "choices" in error_data:
                    # Si hay un mensaje en la respuesta de error, extraerlo
                    content = error_data["choices"][0]["message"]["content"]
                    return content.strip()
                else:
                    return f"Error en la solicitud: {response.status_code}"
            except json.JSONDecodeError:
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
    inputs=gr.Textbox(lines=2, placeholder="Escribe tu mensaje aquí..."),
    outputs=gr.Textbox(label="Respuesta del Chatbot"),
    title="Agente IAma",
    description="Prueba rápida de chatbot usando AI/ML API."
)

# Iniciar la aplicación
if __name__ == "__main__":
    iface.launch()
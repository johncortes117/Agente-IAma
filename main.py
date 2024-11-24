from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import crud, models
from app.database import engine, get_db
from fastapi.responses import HTMLResponse
import requests
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Obtener las variables de entorno
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar templates
templates = Jinja2Templates(directory="app/templates")

# Rutas para las páginas
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/chat")
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/chat-interface")
async def chat_interface():
    return templates.TemplateResponse("gradio_iframe.html", {
        "request": Request,
        "gradio_url": "http://localhost:7860"
    })

# API endpoints
@app.post("/api/users")
async def create_user(user: models.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/api/classes", response_model=models.Class)
async def create_class(
    class_data: models.ClassCreate, 
    user_id: int, 
    db: Session = Depends(get_db)
):
    return crud.create_class(db=db, class_data=class_data, user_id=user_id)

@app.get("/api/users/{user_id}", response_model=models.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/api/chat")
async def chat(request: Request):
    if not API_URL or not API_KEY:
        return {"response": "Error: API_URL o API_KEY no están configurados correctamente."}
        
    data = await request.json()
    message = data.get("message")
    conversation_history = data.get("conversation_history", [])  # Obtener el historial
    
    if not message:
        raise HTTPException(status_code=400, detail="No message provided")
    
    try:
        system_prompt = """Eres un agente de inteligencia artificial que ayuda a los estudiantes a descubrir qué carrera universitaria pueden seguir. 
        Cuando el estudiante se presenta con su información personal, usa esos datos para personalizar tus recomendaciones según su edad y país.
        Pregunta sobre sus materias favoritas, rendimiento académico, intereses y metas profesionales.
        Siempre que hagas preguntas, preséntalas en una lista numerada y sé breve y directo."""
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Construir los mensajes incluyendo el historial
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": message})
        
        payload = {
            "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            try:
                data = response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    content = data["choices"][0]["message"]["content"]
                    return {
                        "response": content.strip(),
                        "conversation_history": messages + [{"role": "assistant", "content": content.strip()}]
                    }
                else:
                    return {"response": "Error: Formato de respuesta inesperado"}
            except Exception as e:
                return {"response": f"Error al procesar la respuesta: {str(e)}"}
        else:
            return {"response": f"Error en la solicitud: {response.status_code}. Detalles: {response.text}"}
                
    except Exception as e:
        return {"response": f"Error de conexión: {str(e)}"}
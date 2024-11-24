import uvicorn
from multiprocessing import Process
from app.chatbot import iface
from main import app

def run_gradio():
    iface.launch(server_name="0.0.0.0", server_port=7860)

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    p1 = Process(target=run_gradio)
    p2 = Process(target=run_fastapi)
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join() 
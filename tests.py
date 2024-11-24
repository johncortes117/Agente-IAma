import requests
import time
import statistics
from dotenv import load_dotenv
import os
import json
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

def test_api_latency(prompt, num_tests=5):
    """
    Realiza múltiples pruebas de latencia a la API.
    
    Args:
        prompt (str): El mensaje para enviar a la API
        num_tests (int): Número de pruebas a realizar
    """
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        "messages": [
            {"role": "system", "content": "Eres un asistente útil."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000,
        "temperature": 0.7,
        "top_p": 1.0
    }
    
    # Lista para almacenar los tiempos de respuesta
    response_times = []
    successful_responses = 0
    failed_responses = 0
    
    # Archivo para guardar los resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"api_latency_test_{timestamp}.log"
    
    print(f"\nIniciando pruebas de latencia ({num_tests} intentos)...")
    print(f"Los resultados se guardarán en: {log_filename}\n")
    
    with open(log_filename, "w", encoding="utf-8") as log_file:
        log_file.write(f"Prueba de latencia API LLaMA - {datetime.now()}\n")
        log_file.write(f"API URL: {API_URL}\n")
        log_file.write(f"Prompt utilizado: {prompt}\n\n")
        
        for i in range(num_tests):
            print(f"Realizando prueba {i+1}/{num_tests}...")
            
            try:
                # Medir tiempo de inicio
                start_time = time.time()
                
                # Realizar la solicitud
                response = requests.post(
                    API_URL,
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                
                # Calcular tiempo total
                end_time = time.time()
                response_time = end_time - start_time
                
                # Procesar respuesta
                if response.status_code in [200, 201]:
                    successful_responses += 1
                    response_times.append(response_time)
                    
                    # Extraer longitud de la respuesta
                    response_data = response.json()
                    response_content = response_data["choices"][0]["message"]["content"]
                    content_length = len(response_content)
                    
                    log_entry = (
                        f"Prueba {i+1}:\n"
                        f"  Tiempo de respuesta: {response_time:.2f} segundos\n"
                        f"  Código de estado: {response.status_code}\n"
                        f"  Longitud de respuesta: {content_length} caracteres\n"
                        f"  Primeros 100 caracteres: {response_content[:100]}...\n\n"
                    )
                else:
                    failed_responses += 1
                    log_entry = (
                        f"Prueba {i+1}:\n"
                        f"  Error - Código de estado: {response.status_code}\n"
                        f"  Respuesta: {response.text[:200]}...\n\n"
                    )
                
                log_file.write(log_entry)
                print(f"  Tiempo de respuesta: {response_time:.2f} segundos")
                
                # Esperar un poco entre solicitudes para no sobrecargar la API
                if i < num_tests - 1:
                    time.sleep(2)
                
            except Exception as e:
                failed_responses += 1
                error_message = f"Prueba {i+1}:\n  Error: {str(e)}\n\n"
                log_file.write(error_message)
                print(f"  Error: {str(e)}")
        
        # Calcular y guardar estadísticas
        if response_times:
            stats = {
                "Promedio": statistics.mean(response_times),
                "Mediana": statistics.median(response_times),
                "Desviación estándar": statistics.stdev(response_times) if len(response_times) > 1 else 0,
                "Mínimo": min(response_times),
                "Máximo": max(response_times),
                "Pruebas exitosas": successful_responses,
                "Pruebas fallidas": failed_responses
            }
            
            log_file.write("\nEstadísticas finales:\n")
            for key, value in stats.items():
                if isinstance(value, float):
                    log_file.write(f"{key}: {value:.2f} segundos\n")
                else:
                    log_file.write(f"{key}: {value}\n")
            
            # Mostrar resumen en consola
            print("\nResumen de resultados:")
            print(f"Tiempo promedio de respuesta: {stats['Promedio']:.2f} segundos")
            print(f"Tiempo mínimo: {stats['Mínimo']:.2f} segundos")
            print(f"Tiempo máximo: {stats['Máximo']:.2f} segundos")
            print(f"Pruebas exitosas: {stats['Pruebas exitosas']}")
            print(f"Pruebas fallidas: {stats['Pruebas fallidas']}")
            print(f"\nResultados detallados guardados en: {log_filename}")

if __name__ == "__main__":
    # Prompt de prueba
    test_prompt = "¿Qué es la inteligencia artificial?"
    
    # Realizar pruebas
    test_api_latency(test_prompt, num_tests=5)
# Agente IAma 🦙🤖

[![Hackathon: Llama Impact PAN LATAM](https://img.shields.io/badge/Hackathon-Llama%20Impact%20PAN%20LATAM-blue)](https://lablab.ai/event/hackathon-llama-impact-pan-latam-es)
[![Licencia: MIT](https://img.shields.io/badge/Licencia-MIT-green)](LICENSE)

**Agente IAma** es un asistente de inteligencia artificial diseñado para ayudar a jóvenes de Latinoamérica a construir su futuro educativo y profesional. Utilizando los avanzados modelos de lenguaje **Llama 3**, IAma combina el análisis de datos académicos, intereses personales y características de personalidad para proporcionar recomendaciones personalizadas de carreras y planes educativos.

## 🌟 Inspiración

El proyecto aborda un problema crítico en la región: muchos estudiantes no saben qué carrera elegir al terminar la secundaria, lo que puede llevar a abandonos tempranos en la universidad. IAma busca empoderar a los jóvenes con orientación informada y personalizada, fomentando decisiones de vida más conscientes.

## 🚀 Funcionalidades Principales

- **Análisis Académico:** Procesa datos de asignaturas y calificaciones para identificar áreas de mayor potencial.
- **Test de Personalidad e Intereses:** Ayuda a conectar los gustos del usuario con carreras afines.
- **Orientación Dinámica:** Responde preguntas y ofrece recursos educativos basados en las necesidades individuales.
- **Compatibilidad Multimodal:** Aprovecha las capacidades avanzadas de **Llama 3** para generar recomendaciones precisas y adaptadas.

## 🛠️ Tecnologías

- **Modelo:** Llama 3.1 405B Instruct Turbo
- **Framework:** Python y FastAPI para el backend.
- **Interfaz:** Bootstrap para el frontend, con un diseño intuitivo y accesible.

💡 Equipo
- John Cortés
- Angelo Benavides

## 📋 Cómo Empezar

Sigue estos pasos para configurar el proyecto localmente:

1. Clona este repositorio:

   ```bash
   git clone https://github.com/johncortes117/agente-iama.git
   cd agente-iama/
   ```
   
2. Crear el ambiente virtual:

   Windows:
   ```bash
   python -m venv env
   ```
   
   Linux/macOS:
   ```bash
   python3 -m venv env
   ```
   
4. Activar el entorno virtual:

   Windows:
   ```bash
   .\env\Scripts\activate
   ```
   
   Linux/macOS:
   ```bash
   source env/bin/activate
   ```
6. Instalar las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

7. Configurar el archivo .env:

   Este proyecto utiliza variables de entorno para configurar el acceso a la API. Para crear el archivo .env con las variables necesarias, ejecuta el siguiente comando en la raíz del 
   proyecto:

   ```bash
   echo "API_URL=tu_url_aqui" > .env
   echo "API_KEY=tu_api_key_aqui" >> .env
   ```

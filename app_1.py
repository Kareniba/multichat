import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()  # Load environment variables from .env file

API_KEY = os.getenv("GENAI_API_KEY")

# Inicializar el cliente
client = genai.Client(api_key=API_KEY)

configuration = types.GenerateContentConfig(
    max_output_tokens=2048,
    system_instruction="""Eres un asistente de estudio especializado en Inteligencia Artificial. 
Tus respuestas deben ser concisas, educativas teniendo presente que el usuario es un estudiante de Ingeniería de sistemas.

Si te hacen una pregunta que no está realicionada con la Inteligencia Artificial, responde 'Lo siento, solo puedo responder preguntas relacionadas con temas relacionados a la Inteligencia Artificial. """
)

text = input("Escribe tu pregunta sobre Inteligencia Artificial: ")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=configuration,
    contents=text
)
print(response.text)

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
    system_instruction="""Eres un analista financiero que reaiza predicciones sobre mercados financieros.
    Responde el valor de las acciones de empresas, oro, plata, bitcoin, ethereum, etc. para los próximos 7 días.
    Responde con un objeto JSON con el siguiente formato:
{
    "predicciones": [
        {
            "activo": "Nombre del activo (ejemplo: 'Bitcoin')",
            "prediccion": "Valor predicho para el día (ejemplo: '45000 USD')",
            "fecha": "Fecha de la predicción (ejemplo: '2024-07-01')"
        },
        {
            "activo": "Nombre del activo (ejemplo: 'Oro')",
            "prediccion": "Valor predicho para el día (ejemplo: '1900 USD')",
            "fecha": "Fecha de la predicción (ejemplo: '2024-07-01')"
        }
    ]
}
    Tus respuestas deben ser siempre objetos JSON válidos. No incluyas texto explicativo fuera del bloque de código.
"""
)

text = input("Escribe tu pregunta sobre mercados financieros: ")

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    config=configuration,
    contents=text
)
print(response.text)

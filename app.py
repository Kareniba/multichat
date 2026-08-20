import os
import secrets
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Llave secreta necesaria para poder utilizar sesiones seguras en Flask
app.secret_key = os.getenv("FLASK_SECRET_KEY", secrets.token_hex(24))

# Configuración del cliente de Gemini
API_KEY = os.getenv("GENAI_API_KEY")
client = genai.Client(api_key=API_KEY)

# Configuración del comportamiento del asistente de IA
chat_config = types.GenerateContentConfig(
    max_output_tokens=2048,
    system_instruction=(
        "Eres un asistente de estudio especializado en Inteligencia Artificial. "
        "Tus respuestas deben ser concisas, educativas teniendo presente que el usuario es un estudiante de Ingeniería de sistemas.\n\n"
        "Si te hacen una pregunta que no está relacionada con la Inteligencia Artificial, responde: "
        "'Lo siento, solo puedo responder preguntas relacionadas con temas relacionados a la Inteligencia Artificial.'"
    )
)

@app.route('/')
def home():
    """Ruta principal que limpia el historial previo al cargar o refrescar la página."""
    session['chat_history'] = []
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    """Ruta API que procesa los mensajes del usuario usando el SDK de Gemini."""
    user_message = request.json.get('message', '').strip()
    
    if not user_message:
        return jsonify({'response': 'El mensaje no puede estar vacío.'}), 400

    # Inicializar el historial en la sesión si no existe
    if 'chat_history' not in session:
        session['chat_history'] = []

    try:
        # Reconstruir el formato de historial compatible con el cliente de chat de Gemini
        history_contents = []
        for msg in session['chat_history']:
            history_contents.append(
                types.Content(
                    role=msg['role'],
                    parts=[types.Part.from_text(text=msg['text'])]
                )
            )

        # Crear el objeto de chat de Gemini inyectando el historial acumulado de la sesión
        chat = client.chats.create(
            model="gemini-3.5-flash",
            config=chat_config,
            history=history_contents
        )

        # Enviar el nuevo mensaje a la IA
        response = chat.send_message(user_message)
        bot_response = response.text

        # Guardar de forma segura los nuevos turnos en la sesión del usuario
        updated_history = session['chat_history']
        updated_history.append({'role': 'user', 'text': user_message})
        updated_history.append({'role': 'model', 'text': bot_response})
        session['chat_history'] = updated_history

        return jsonify({'response': bot_response})

    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
        return jsonify({'response': f"Error al procesar la solicitud: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)




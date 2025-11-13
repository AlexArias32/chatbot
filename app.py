from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Carga la clave de OpenAI desde .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Página principal
@app.route("/")
def home():
    return render_template("index.html")

# Ruta para procesar preguntas
@app.route("/preguntar", methods=["POST"])
def preguntar():
    data = request.get_json()
    pregunta = data.get("mensaje", "")

    # Prompt para ChatGPT
    prompt = f"""
    Eres un asesor de soporte técnico experto en Windows, macOS, redes e instalación de software.
    Responde de forma clara y paso a paso.
    Usuario: {pregunta}
    """

    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        # Acceso correcto a la respuesta
        texto = respuesta.choices[0].message.content
        return jsonify({"respuesta": texto})

    except Exception as e:
        print("Error en la API:", e)

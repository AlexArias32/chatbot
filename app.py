from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Carga variables de entorno localmente
load_dotenv()

# Inicializa API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Página principal
@app.route("/")
def home():
    return render_template("index.html")

# Ruta para preguntas
@app.route("/preguntar", methods=["POST"])
def preguntar():
    data = request.get_json()
    pregunta = data.get("mensaje", "")

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
        return jsonify({"respuesta": f"⚠️ Ocurrió un error procesando tu solicitud: {e}"})

# Solo se ejecuta en local (modo debug)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

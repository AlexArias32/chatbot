from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/preguntar", methods=["POST"])
def preguntar():
    data = request.get_json()
    pregunta = data.get("mensaje", "")

    prompt = f"""
    Eres un asesor de soporte técnico experto en Windows, macOS, redes e instalación de software.
    Ofrece soluciones paso a paso, de forma clara y amable.
    Usuario: {pregunta}
    """

    respuesta = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    texto = respuesta.choices[0].message.content
    return jsonify({"respuesta": texto})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

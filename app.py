from flask import Flask,render_template, request, Response
import google.generativeai as genai
from dotenv import load_dotenv
import os
from time import sleep

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
modelo = "gemini-1.5-flash"   
genai.configure(api_key=api_key)

app = Flask(__name__)
app.secret_key = 'aluralatam'

def bot(prompt):
    #número máximo de intentos 
    max_intentos = 1
    repeticion = 0
    while True:
        try:
            prompt_sistema = """Eres un chatbot de atención al cliente de una e-commerce. No debes
                                responder preguntas que no sean referentes a los datos del ecommerce 
                                informado."""
            
            configuracion_modelo = {
                "temperature":0.2,
                "max_output_tokens": 8192
            }

            llm = genai.GenerativeModel(
                model_name = modelo,
                system_instruction = prompt_sistema,
                generation_config = configuracion_modelo   
            )

            respuesta = llm.generate_content(prompt)
            return respuesta.text
        
        except Exception as e:
            repeticion += 1
            if repeticion >= max_intentos:
                return "Error con Gemini: %s" % e
            sleep(50)

@app.route("/chat", methods=["POST"]) #Estamos creando la ruta hacia el endpoint /chat que va a invocar el metodo POST 
def chat():
    prompt = request.json["msg"]
    respuesta = bot(prompt)
    return respuesta

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)

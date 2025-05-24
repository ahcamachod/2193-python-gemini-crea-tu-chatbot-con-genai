from flask import Flask,render_template, request, Response
import google.generativeai as genai
from dotenv import load_dotenv
import os
from time import sleep
from utils import carga, guarda
from personas import personas, seleccionar_persona
from gestion_historial import eliminar_mensajes_antiguos

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
modelo = "gemini-1.5-flash"   
genai.configure(api_key=api_key)

app = Flask(__name__)
app.secret_key = 'aluralatam'

contexto = carga("datos/musicmart.txt")

def crear_chatbot():
    personalidad = "neutro"
    prompt_sistema = f"""
                        # PERSONA

                        Eres un chatbot de atención al cliente de una e-commerce. No debes
                        responder preguntas que no sean referentes a los datos del ecommerce 
                        informado.

                        Únicamente debes de utilizar los datos que estén dentro del 'contexto'.

                        # CONTEXTO
                        {contexto}

                        # PERSONALIDAD
                        {personalidad}

                        # HISTORIAL
                        Accede siempre al historial de mensajes, y recupera las informaciones previamente
                        mencionadas.
                    """
    configuracion_modelo = {
        "temperature":0.2,
        "max_output_tokens": 8192
    }

    llm = genai.GenerativeModel(
        model_name = modelo,
        system_instruction = prompt_sistema,
        generation_config = configuracion_modelo   
    )    

    chatbot = llm.start_chat(history=[]) 
    return chatbot

chatbot = crear_chatbot()

def bot(prompt):
    #número máximo de intentos 
    max_intentos = 1
    repeticion = 0
    while True:
        try:
            personalidad = personas[seleccionar_persona(prompt)]
            mensaje_usuario = f"""
                                 Considera esta personalidad para responder al mensaje:
                                 {personalidad}.

                                 Responde al mensaje siguiente, siempre recordando el historial:
                                 {prompt}
                               """
            respuesta = chatbot.send_message(mensaje_usuario)
            if len(chatbot.history) > 4:
                chatbot.history = eliminar_mensajes_antiguos(chatbot.history)
            print(f'Cantidad de mensajes: {len(chatbot.history)}\n{chatbot.history}') 
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

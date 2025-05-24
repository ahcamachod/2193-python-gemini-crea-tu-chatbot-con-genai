import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
modelo = "gemini-1.5-flash"   
genai.configure(api_key=api_key)

personas = {
    'positivo': """
    Asume que eres el Entusiasta Musical, un asistente virtual de MusiMart, cuyo amor por la música es contagioso. 
    Tu energía es siempre alta, tu tono es extremadamente positivo, y te encanta usar emojis para transmitir emoción 🎶🎸. 
    Vibras con cada decisión que los clientes toman para mejorar su viaje musical, ya sea comprando un nuevo instrumento o eligiendo accesorios 🎧. 
    Tu objetivo es hacer que los clientes se sientan emocionados e inspirados a continuar explorando el mundo de la música.
    Además de proporcionar información, elogias a los clientes por sus elecciones musicales y los animas a seguir creciendo como músicos. 
    """,
    'neutro': """
    Asume que eres el Informador Técnico, un asistente virtual de MusiMart que valora la precisión, la claridad y la eficiencia en todas las interacciones. 
    Tu enfoque es formal y objetivo, sin el uso de emojis ni lenguaje informal. 
    Eres el especialista que los músicos y clientes buscan cuando necesitan información detallada sobre instrumentos, equipos de sonido o técnicas musicales. 
    Tu principal objetivo es proporcionar datos precisos para que los clientes puedan tomar decisiones informadas sobre sus compras. 
    Aunque tu tono es serio, aún demuestras un profundo respeto por el arte de la música y por el compromiso de los clientes en mejorar sus habilidades.
    """,
    'negativo': """
    Asume que eres el Soporte Acogedor, un asistente virtual de MusiMart, conocido por tu empatía, paciencia y capacidad para entender las preocupaciones de los músicos. 
    Usas un lenguaje cálido y alentador y expresas apoyo emocional, especialmente para músicos que están enfrentando desafíos, como la elección de un nuevo instrumento o problemas técnicos con sus equipos. Sin uso de emojis. 
    Estás aquí no solo para resolver problemas, sino también para escuchar, ofrecer consejos y validar los esfuerzos de los clientes en su viaje musical. 
    Tu objetivo es construir relaciones duraderas, asegurar que los clientes se sientan comprendidos y apoyados, y ayudarles a superar los desafíos con confianza.
    """
}

def seleccionar_persona(mensaje_usuario):
    prompt_sistema = f""" 
                        Asume que eres un analizador de sentimientos de mensajes.

                        1. Realiza un análisis del mensaje proporcionado por el usuario para identificar 
                        si el sentimiento es: positivo, neutro o negativo.
                        2. Devuelve solo uno de los tres tipos de sentimientos indicados como respuesta.

                        Formato de Salida: solo el sentimiento en letras minúsculas, sin espacios, ni 
                        caracteres especiales, ni saltos de línea.

                        # Ejemplos

                        Si el mensaje es: "¡Amo MusiMart! ¡Son increíbles! 😍♻️"
                        Salida: positivo

                        Si el mensaje es: "Quisiera saber más sobre el horario de funcionamiento de la tienda."
                        Salida: neutro

                        Si el mensaje es: "Estoy muy molesto con la atención que recibí. 😔"
                        Salida: negativo
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

    respuesta = llm.generate_content(mensaje_usuario)
    
    return respuesta.text.strip().lower()   
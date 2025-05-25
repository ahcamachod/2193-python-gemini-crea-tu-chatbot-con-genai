import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
modelo = "gemini-1.5-flash"   
genai.configure(api_key=api_key)

def generar_imagen_gemini(camino_imagen):
    archivo_temporal = genai.upload_file(
        path = camino_imagen,
        display_name = 'Imagen Enviada'
    )
    print(f'Imagen Enviada: {archivo_temporal.uri}')
    return archivo_temporal
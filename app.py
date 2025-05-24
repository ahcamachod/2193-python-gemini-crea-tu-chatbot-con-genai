from flask import Flask,render_template, request, Response
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
modelo = "gemini-1.5-flash"   
genai.configure(api_key=api_key)

app = Flask(__name__)
app.secret_key = 'aluralatam'

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)

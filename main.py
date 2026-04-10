from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
import requests

# 🚀 Inicializar app
app = FastAPI()

# 🔑 Cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 📩 Modelo de entrada
class Mensaje(BaseModel):
    message: str

# 🔌 Función para consultar SQL (API local con ngrok)
def consultar_sql(query):
    try:
        url = "https://pureness-dig-magnetize.ngrok-free.dev/query"
        response = requests.get(url, params={"sql": query}, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# 🏠 Endpoint base
@app.get("/")
def home():
    return {"status": "FSQ AI funcionando 🚀"}

# 🤖 Webhook principal
@app.post("/webhook")
async def webhook(data: Mensaje):

    try:
        mensaje = data.message

        # 🧠 Generar SQL con IA
        prompt = f"""
        Eres un experto en SQL Server.

        Convierte la siguiente pregunta en una consulta SQL válida:
        {mensaje}

        Reglas:
        - Usa SELECT solamente
        - No uses DELETE, UPDATE, INSERT
        - Usa TOP si es necesario
        - Responde SOLO con SQL limpio, sin explicación
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        query_sql = response.choices[0].message.content.strip()

        # 🔒 Validación básica de seguridad
        if any(word in query_sql.lower() for word in ["delete", "update", "insert", "drop"]):
            return {"error": "Consulta no permitida"}

        # 🔌 Ejecutar consulta en SQL Server
        datos = consultar_sql(query_sql)

        return {
            "pregunta": mensaje,
            "query_generado": query_sql,
            "resultado": datos
        }

    except Exception as e:
        return {
            "error": str(e)
        }
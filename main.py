from fastapi import FastAPI
from pydantic import BaseModel
import requests
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key="TU_API_KEY")

class Mensaje(BaseModel):
    message: str


@app.post("/webhook")
async def webhook(data: Mensaje):

    mensaje = data.message

    # 1. Generar SQL
    prompt = f"""
    Eres experto en SQL Server.

    Tabla ventas:
    - id
    - fecha
    - total
    - cliente

    Convierte esta pregunta en SQL:
    {mensaje}

    Responde SOLO SQL válido.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    query_sql = response.choices[0].message.content.strip()

    # 2. Ejecutar SQL
    try:
        url = "https://pureness-dig-magnetize.ngrok-free.dev/query"
        datos = requests.get(url, params={"sql": query_sql}, timeout=8).json()
    except Exception as e:
        return {"error_sql": str(e)}

    return {
        "query": query_sql,
        "datos": datos
    }
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import requests
import os

app = FastAPI()

# 🔐 API KEY desde Railway
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 📩 Modelo de entrada
class Mensaje(BaseModel):
    message: str


@app.post("/webhook")
async def webhook(data: Mensaje):

    try:
        mensaje = data.message

        # =========================
        # 🧠 1. GENERAR SQL
        # =========================
        prompt = f"""
        Eres experto en SQL Server.

        La tabla principal se llama ALBVENTACAB.

        Columnas disponibles:
        - NUMSERIE
        - NUMALBARAN
        - FECHA
        - TOTALNETO
        - TOTAL
        - FO
        - CLIENTE

        Convierte la pregunta del usuario en SQL Server válido.

        Reglas:
        - Usa SOLO columnas existentes
        - Usa SELECT solamente
        - No uses INSERT, UPDATE o DELETE
        - Usa TOP 10 cuando aplique
        - Para ventas totales usa TOTALNETO
        - Usa filtros de fecha eficientes
        - No uses markdown ni explicaciones
        - Responde SOLO SQL

        Pregunta:
        {mensaje}
        """

        response_sql = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        # 🔥 limpiar por si acaso
        query_sql = response_sql.choices[0].message.content.strip()
 
        # limpiar basura tipo ```sql
        query_sql = query_sql.replace("```sql", "").replace("```", "").strip()

        # =========================
        # 🗄️ 2. CONSULTAR SQL SERVER (ngrok)
        # =========================
        try:
            url = "https://pureness-dig-magnetize.ngrok-free.dev/query"
            response_db = requests.get(url, params={"sql": query_sql}, timeout=30)

            datos = response_db.json()

        except Exception as e:
            return {
                "error_sql": str(e),
                "query": query_sql
            }

        # =========================
        # 🧠 3. RESPUESTA INTELIGENTE
        # =========================
        prompt_respuesta = f"""
        Eres un analista de negocios experto.

        Pregunta del usuario:
        {mensaje}

        Datos obtenidos:
        {datos}

        Explica los resultados de forma clara, breve y profesional.
        """

        response_texto = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_respuesta}]
        )

        texto = response_texto.choices[0].message.content.strip()

        return {
            "respuesta": texto,
            "query_usada": query_sql
        }

    except Exception as e:
        return {
            "error_general": str(e)
        }
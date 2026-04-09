from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Mensaje(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "FSQ AI funcionando 🚀"}

@app.post("/webhook")
async def webhook(data: Mensaje):

    try:
        mensaje = data.message

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": mensaje}
            ]
        )

        return {
            "respuesta": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "error": str(e)
        }
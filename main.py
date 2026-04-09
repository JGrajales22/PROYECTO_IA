from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

# 👇 DEFINIMOS EL JSON CORRECTAMENTE
class Mensaje(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "FSQ AI funcionando 🚀"}

@app.post("/webhook")
async def webhook(data: Mensaje):
    
    mensaje = data.message

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": mensaje}]
    )

    return {
        "respuesta": response["choices"][0]["message"]["content"]
    }
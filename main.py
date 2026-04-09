from fastapi import FastAPI, Request
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def home():
    return {"status": "FSQ AI funcionando 🚀"}

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()

    mensaje = data.get("message", "Hola")

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": mensaje}]
    )

    return {
        "respuesta": response["choices"][0]["message"]["content"]
    }
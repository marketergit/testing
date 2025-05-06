from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import httpx

load_dotenv()

app = FastAPI()

# CORS setup for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_URL = "https://api.deepseek.com"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    message = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "user", "content": message}
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GROQ_API_URL, headers=headers, json=payload)
        result = response.json()

    return {"reply": result["choices"][0]["message"]["content"]}

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/confess")
async def confess(soul: str = Form(...)):
    api_key = os.getenv("OMDB_API_KEY")
    url = f"http://www.omdbapi.com/?t={soul}&apikey={api_key}"

    response = requests.get(url)
    data = response.json()

    if data.get("Response") == "True":
        summary = data.get("Plot", "No plot found.")
        return {"omdb_fact": summary}
    else:
        return {"omdb_fact": "Bart finds no trace of that film in the abyss."}

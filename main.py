from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

OMDB_API_KEY = os.getenv("OMDB_API_KEY", "demo")  # Replace "demo" with your key if not using .env

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "result": None})

@app.post("/", response_class=HTMLResponse)
async def process_form(request: Request, soul: str = Form(...)):
    query = soul.strip()
    if not query:
        result = "Bart hears nothing. Try again."
    else:
        response = requests.get(
            "https://www.omdbapi.com/",
            params={"apikey": OMDB_API_KEY, "t": query}
        )
        data = response.json()
        result = data.get("Plot") or f"Bart found nothing for '{query}'."

    return templates.TemplateResponse("chat.html", {"request": request, "result": result})

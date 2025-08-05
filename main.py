from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "response": "", "input_text": ""})

@app.post("/", response_class=HTMLResponse)
async def post_form(request: Request, soul: str = Form(...)):
    omdb_response = requests.get(f"http://www.omdbapi.com/?t={soul}&apikey={OMDB_API_KEY}")
    if omdb_response.status_code == 200:
        data = omdb_response.json()
        fact = data.get("Plot", "Bart found no plot to unearth.")
    else:
        fact = "Bart could not reach the archives beyond."

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "response": fact,
        "input_text": soul
    })

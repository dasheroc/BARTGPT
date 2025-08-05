from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
def post_form(request: Request, soul: str = Form(...)):
    response_text = None

    if OMDB_API_KEY:
        params = {"t": soul.strip(), "apikey": OMDB_API_KEY}
        res = requests.get("http://www.omdbapi.com/", params=params)

        if res.status_code == 200:
            data = res.json()
            if data.get("Response") == "True":
                response_text = data.get("Plot")
            else:
                response_text = "Bart found nothing. Not even shadows."
        else:
            response_text = "Bart is tired. OMDb didn’t answer."

    else:
        response_text = "Bart requires an OMDB_API_KEY. This is beneath him."

    return templates.TemplateResponse("chat.html", {"request": request, "response": response_text})

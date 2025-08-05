from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

film_facts = [
    {
        "title": "There’s Something About Mary (1998)",
        "summary": "A man gets a chance to meet up with his dream girl from high school, even though his date with her back then was a complete disaster."
    },
    {
        "title": "Hello, My Name Is Doris (2015)",
        "summary": "A self-help seminar inspires a sixty-something woman to romantically pursue her younger co-worker."
    },
    {
        "title": "Synecdoche, New York (2008)",
        "summary": "A theater director builds a life-size replica of New York inside a warehouse as part of his new play."
    }
]

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "response": ""})

@app.post("/", response_class=HTMLResponse)
async def handle_form(request: Request, message: str = Form(...)):
    film = random.choice(film_facts)
    response = f'Bart speaks from the abyss: “{film["title"]}: {film["summary"]}” — curious. But not clever.'
    return templates.TemplateResponse("chat.html", {"request": request, "response": response})

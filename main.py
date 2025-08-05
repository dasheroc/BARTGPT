from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import random
import datetime
import requests

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

oracle_tones = [
    "Bart speaks from the abyss:",
    "The oracle intones without irony:",
    "With a sigh, Bart replies:",
    "Bart does not blink as he says:",
    "From the void, a murmur:"
]

@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "response": None})


def fetch_film_data(title: str) -> str:
    url = "http://www.omdbapi.com/"
    params = {
        "apikey": OMDB_API_KEY,
        "t": title
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("Response") == "False":
        return f"No results for “{title}.” Bart exhales slowly."

    title = data.get("Title", "Unknown")
    year = data.get("Year", "????")
    director = data.get("Director", "???")
    plot = data.get("Plot", "No summary. Just vibes.")

    return f"{title} ({year}) — Directed by {director}. {plot}"


@app.post("/sealema", response_class=HTMLResponse)
async def post_sealema(request: Request, user_input: str = Form(...)):
    user_text = user_input.strip().lower()

    if not user_text:
        response = "You said nothing. Bart is unimpressed."

    elif user_text.startswith("film:"):
        title = user_input.split(":", 1)[1].strip()
        response = fetch_film_data(title)

    else:
        response = f"“{user_input}” — curious. But not clever."

    final_output = f"{random.choice(oracle_tones)} {response}"

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "response": final_output
    })

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import random

app = FastAPI()

# Jinja2 template directory
templates = Jinja2Templates(directory="templates")

# Static assets (favicon etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root alive check
@app.get("/")
def root():
    return {
        "message": "BartGPT API is alive. Try /docs for the interface.",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# Randomized seal fact route
@app.get("/bart/seal")
def seal_fact():
    facts = [
        "Seals can sleep underwater by shutting off half their brain.",
        "Some seals can dive over 1,500 feet deep.",
        "Seal pups can recognize their mother's voice just days after birth.",
        "A group of seals on land is called a harem.",
        "Seals clap underwater—not to applaud, but to warn rivals."
    ]
    return {"seal_fact": random.choice(facts)}

# Judgment route for cinephilic taste
@app.get("/bart/film")
def film_opinion(title: str = "Suspiria"):
    match title.lower():
        case "suspiria":
            return {"judgment": "Correct. Bart nods."}
        case "fargo":
            return {"judgment": "Acceptable. Bart squints."}
        case _:
            return {"judgment": "Wrong. Bart sighs."}

# Sealema GET: render the HTML interface
@app.get("/sealema", response_class=HTMLResponse)
async def get_sealema(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

# Sealema POST: respond to user's unburdening
@app.post("/sealema", response_class=HTMLResponse)
async def post_sealema(request: Request, user_input: str = Form(...)):
    response = f"Bart has received your unburdening: “{user_input}.” His eyebrow arches—just slightly."
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "response": response
    })

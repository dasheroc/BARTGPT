from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import random

app = FastAPI()

# Jinja2 template directory
templates = Jinja2Templates(directory="templates")

# Mount static assets
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root
@app.get("/")
def root():
    return {
        "message": "BartGPT API is alive. Try /docs for the interface.",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# Seal fact API
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

# Film judgment API
@app.get("/bart/film")
def film_opinion(title: str = "Suspiria"):
    match title.lower():
        case "suspiria":
            return {"judgment": "Correct. Bart nods."}
        case "fargo":
            return {"judgment": "Acceptable. Bart squints."}
        case _:
            return {"judgment": "Wrong. Bart sighs."}

# Sealema GET interface
@app.get("/sealema", response_class=HTMLResponse)
async def get_sealema(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

# Sealema POST interface – response engine engaged
@app.post("/sealema", response_class=HTMLResponse)
async def post_sealema(request: Request, user_input: str = Form(...)):

    user_text = user_input.strip().lower()

    oracle_tones = [
        "Bart speaks from the abyss:",
        "The lights flicker. He responds:",
        "Your words echo. His reply follows:",
        "A pause. Then judgment:",
        "The air stiffens. Bart intones:"
    ]

    if "seal" in user_text:
        response = random.choice([
            "Seals slap each other to show dominance. As should we all.",
            "A harem of seals is louder than a Cannes afterparty.",
            "Seal pups wail like they're in a Bergman film. Bart relates.",
            "They nap underwater. A talent you should cultivate.",
            "Some seals can dive to 1,500 feet—deeper than your last relationship."
        ])
    elif "film" in user_text or "movie" in user_text or "cinema" in user_text:
        response = random.choice([
            "If it isn't shot in 4:3 or French, Bart barely considers it cinema.",
            "You want a film recommendation? Watch something that hurts.",
            "All great films involve guilt, silence, or weather.",
            "Cinema is ritual. You're still watching content.",
            "There is no cinema left. Only algorithmic moodboards with budgets."
        ])
    elif "who are you" in user_text or "what is this" in user_text:
        response = "This is Sealema. An oracle in a trench coat, wrapped in film stock and seal blubber."
    elif user_text in ["", " "]:
        response = "You said nothing. Bart is unimpressed."
    else:
        response = f"“{user_input}” — curious. But not clever."

    final_output = f"{random.choice(oracle_tones)} {response}"

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "response": final_output
    })

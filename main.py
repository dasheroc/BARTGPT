from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import random
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

oracle_tones = [
    "Bart whispers through gritted teeth:",
    "Bart shrugs and lights a clove cigarette:",
    "Bart closes the book mid-sentence and says:",
    "Bart, unimpressed but intrigued, remarks:",
    "Bart mutters like an overeducated ghost:",
    "Bart speaks from the abyss:"
]

@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "response": ""})

@app.post("/sealema", response_class=HTMLResponse)
async def post_sealema(request: Request, user_input: str = Form(...)):
    if not user_input.strip():
        response = "You said nothing. Bart is unimpressed."
    elif user_input.lower().startswith("film:"):
        query = user_input[5:].strip()
        if OMDB_API_KEY:
            api_url = f"http://www.omdbapi.com/?t={query}&apikey={OMDB_API_KEY}"
            res = requests.get(api_url)
            if res.status_code == 200:
                data = res.json()
                if data.get("Response") == "True":
                    response = (
                        f"**{data['Title']}** ({data['Year']})\n"
                        f"Directed by {data.get('Director', 'Unknown')}.\n"
                        f"Plot: {data.get('Plot', 'No summary available.')}"
                    )
                else:
                    response = f"No film found matching '{query}'. Try again—clearly, you're thinking of something obscure."
            else:
                response = "OMDb query failed. Bart raises an eyebrow at your API reliability."
        else:
            response = "OMDb API key missing. Bart refuses to proceed without credentials."
    else:
        response = f"“{user_input}” — curious. But not clever."

    final_output = f"{random.choice(oracle_tones)} {response}"
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "response": final_output
    })

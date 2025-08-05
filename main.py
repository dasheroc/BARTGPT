from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Mount static directory for favicon, fonts, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def post_form(request: Request, soul: str = Form(...)):
    ui = soul.strip()
    if not OMDB_API_KEY:
        reply = "⚠️ OMDb key missing. Bart is silent."
    else:
        try:
            resp = requests.get("https://www.omdbapi.com/", params={"apikey": OMDB_API_KEY, "t": ui})
            data = resp.json()
            if data.get("Response") == "True":
                title = data.get("Title") or "Unknown"
                year = data.get("Year") or "N/A"
                plot = data.get("Plot") or ""
                reply = f"{title} ({year}): {plot}"
            else:
                reply = f"No film found for '{ui}'. Bart shrugs."
        except Exception as e:
            reply = f"Error fetching film: {e}"
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "response": reply,
        "input": ui
    })

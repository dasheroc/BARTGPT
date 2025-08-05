from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Static & template setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

OMDB_API_KEY = os.getenv("OMDB_API_KEY")  # Ensure this is set in your .env

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/confess")
async def confess(soul: str = Form(...)):
    omdb_url = f"http://www.omdbapi.com/?t={soul}&apikey={OMDB_API_KEY}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(omdb_url)
            data = response.json()
            if data.get("Response") == "True":
                title = data.get("Title", "Unknown")
                plot = data.get("Plot", "No plot available.")
                return JSONResponse(content={"response": f"*{title}* — {plot}"})
            else:
                return JSONResponse(content={"response": f"Nothing found for '{soul}' — try again, preferably with better taste."})
        except Exception:
            return JSONResponse(content={"response": "Bart cannot reach OMDb. Perhaps the abyss is down."})

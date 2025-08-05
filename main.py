from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

OMDB_API_KEY = os.getenv("OMDB_API_KEY")  # You must set this in Render's environment

@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def post_chat(request: Request, user_input: str = Form(...)):
    try:
        async with httpx.AsyncClient() as client:
            params = {"s": user_input, "apikey": OMDB_API_KEY}
            r = await client.get("http://www.omdbapi.com/", params=params)
            data = r.json()

        if data.get("Response") == "True":
            film = data["Search"][0]
            title = film["Title"]
            year = film["Year"]

            # Get full plot
            async with httpx.AsyncClient() as client:
                params = {"t": title, "y": year, "apikey": OMDB_API_KEY, "plot": "short"}
                r = await client.get("http://www.omdbapi.com/", params=params)
                details = r.json()

            response = f"{title} ({year}): {details.get('Plot', 'No plot found.')}"
        else:
            response = "Nothing surfaced from the abyss. Try again."

    except Exception:
        response = "The void muttered an error. Try again later."

    return templates.TemplateResponse("chat.html", {"request": request, "response": response})

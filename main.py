from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import requests

app = FastAPI()

# Mount static directory for favicon and other assets
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def post_form(request: Request, soul: str = Form(...)):
    user_input = soul.strip()
    response_text = ""

    if OMDB_API_KEY and user_input:
        omdb_url = f"http://www.omdbapi.com/?t={user_input}&apikey={OMDB_API_KEY}"
        try:
            res = requests.get(omdb_url)
            data = res.json()

            if data.get("Response") == "True":
                response_text = (
                    f"🎬 <strong>{data.get('Title')}</strong> ({data.get('Year')})<br>"
                    f"⭐ <em>{data.get('imdbRating')}/10</em> on IMDb<br>"
                    f"📜 {data.get('Plot')}<br>"
                    f"🎥 Directed by: {data.get('Director')}<br>"
                    f"🎭 Starring: {data.get('Actors')}"
                )
            else:
                response_text = f"🐚 Alas, no film by the name of ‘{user_input}’ could be conjured."

        except Exception as e:
            response_text = f"⚠️ The Oracle stammered: {str(e)}"
    else:
        response_text = "🐚 Bart contemplates in silence. Say something of substance."

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "response": response_text,
        "original": user_input
    })

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import requests

app = FastAPI()

# --- Static File Mounting ---
static_dir = "static"
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
else:
    print(f"⚠️ Static directory '{static_dir}' not found at startup.")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def post_form(request: Request, query: str = Form(...)):
    api_key = os.getenv("OMDB_API_KEY")
    if not api_key:
        return templates.TemplateResponse("chat.html", {
            "request": request,
            "result": "⚠️ OMDB API key is missing. Check environment settings."
        })

    url = f"http://www.omdbapi.com/?apikey={api_key}&t={query}"
    try:
        response = requests.get(url)
        data = response.json()
        result = data.get("Plot", "No plot found.") if data.get("Response") == "True" else "Movie not found."
    except Exception as e:
        result = f"Error retrieving data: {e}"

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "result": result
    })

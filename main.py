from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()

# Mount static files (this is what Jinja2's url_for('static', ...) depends on)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates directory
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def post_chat(request: Request, user_input: str = Form(...)):
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "user_input": user_input
    })

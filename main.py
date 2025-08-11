from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import openai, os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/sealema", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/sealema", response_class=HTMLResponse)
async def respond(request: Request, prompt: str = Form(...)):
    try:
        reply = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're Bart, a cryptic, sarcastic film AI that responds with wit and cinematic references."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        ).choices[0].message.content.strip()
    except Exception as e:
        reply = f"Bart crashed. Probably your fault. ({e})"

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "response": reply,
        "prompt": prompt
    })

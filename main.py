from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/sealema", response_class=HTMLResponse)
async def get_sealema(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/sealema", response_class=HTMLResponse)
async def post_sealema(request: Request, user_input: str = Form(...)):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are BART, a moody gothic AI who responds with cryptic snark."},
            {"role": "user", "content": user_input}
        ]
    )
    output = response.choices[0].message.content.strip()
    return templates.TemplateResponse("chat.html", {"request": request, "response": output})

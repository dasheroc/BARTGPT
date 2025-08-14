from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/sealema", response_class=HTMLResponse)
async def serve_form(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.post("/sealema", response_class=HTMLResponse)
async def handle_chat(request: Request, user_input: str = Form(...)):
    if not user_input.strip():
        reply = "Bart refuses to respond to silence."
    else:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are Bart: poetic, gothic, and slightly condescending."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.9,
                max_tokens=200
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"Bart encountered an error in the void: {str(e)}"

    return templates.TemplateResponse("chat.html", {"request": request, "user_input": user_input, "reply": reply})

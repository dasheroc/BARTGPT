from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import random

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (if needed)
app.mount("/static", StaticFiles(directory="static"), name="static")


class Message(BaseModel):
    text: str


sassy_remarks = [
    "That’s... something. Try again, sweetheart.",
    "Wow. Ever thought about not saying that out loud?",
    "Bart is *bored*. Impress me.",
    "Cryptic. But not in a cool way.",
    "Oh no... you typed *that*?",
    "Bart blinks. Slowly. Judgingly.",
    "Try again. With flair, please.",
    "That's about as clear as mud.",
    "Bart sighs. A deep, eternal sigh.",
    "Hmm. And you were doing so well.",
    "Bart mutters, 'Even I expected better.'",
]

@app.get("/", response_class=HTMLResponse)
async def get_form():
    with open("chat.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/sealema")
async def sealema_endpoint(message: Message):
    response = random.choice(sassy_remarks)
    return JSONResponse(content={"response": f'Bart speaks from the abyss: "{message.text}" — {response}'})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

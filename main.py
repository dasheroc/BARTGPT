from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# Tell FastAPI where your templates are
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def receive_judgment(request: Request, soul: str = Form(...)):
    # Placeholder logic — customize this
    if "excuse" in soul.lower():
        judgment = "Bart disapproves. Try again."
    else:
        judgment = f"Your soul has been judged: {soul.strip().capitalize()}."

    return templates.TemplateResponse(
        "chat.html", {"request": request, "judgment": judgment}
    )


# For local testing only
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000)

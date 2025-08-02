from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# Templates location
templates = Jinja2Templates(directory="templates")

# Serve static files (if needed later)
app.mount("/static", StaticFiles(directory="static"), name="static")


# GET: Home route – shows the form
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


# POST: Handles submitted soul
@app.post("/", response_class=HTMLResponse)
async def receive_judgment(request: Request, soul: str = Form(...)):
    if "excuse" in soul.lower():
        judgment = "Bart disapproves. Try again."
    else:
        judgment = "Bart nods imperceptibly. Approved."

    return templates.TemplateResponse(
        "chat.html", {"request": request, "judgment": judgment}
    )


# Run locally with: python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)

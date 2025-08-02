from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.get("/bart/feelings")
async def bart_feelings(mood: str):
    match mood.lower():
        case "elated":
            return {"response": "Bart pirouettes silently. Joy is a silent scream."}
        case "tired":
            return {
                "response": "Bart stares into the abyss. It stares back with decaf."
            }
        case "apathetic":
            return {
                "response": "'Feeling' is a strong word. Bart barely registers you."
            }
        case _:
            return {
                "response": f"Bart does not recognize the emotion '{mood}'. Try again... or don’t."
            }

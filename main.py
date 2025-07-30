from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "BartGPT API is alive. Try /docs for the interface.",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.get("/bart/seal")
def seal_fact():
    return {
        "seal_fact": "A group of seals on land is called a harem. Bart judges the naming committee."
    }

@app.get("/bart/film")
def film_opinion(title: str = "Suspiria"):
    match title.lower():
        case "suspiria":
            return {"judgment": "Correct. Bart nods."}
        case "fargo":
            return {"judgment": "Acceptable. Bart squints."}
        case _:
            return {"judgment": "Wrong. Bart sighs."}

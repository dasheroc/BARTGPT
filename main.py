from fastapi import FastAPI

app = FastAPI()


@app.get("/bart/film")
def film_opinion(title: str = "Suspiria"):
    match title.lower():
        case "suspiria" | "fargo":
            return {"judgment": "Acceptable. Bart squints."}
        case _:
            return {"judgment": "Wrong. Bart sighs."}


@app.get("/bart/feelings")
def bart_feelings(mood: str):
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

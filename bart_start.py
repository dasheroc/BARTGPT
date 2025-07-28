from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from BARTAPI!"}

@app.get("/bart")
def bart_judgment(name: str = "Rashad"):
    mood = "highly skeptical"
    return {"bart": f"Good day, {name}. Bart is {mood}."}

@app.get("/bart/advise")
def bart_advise(topic: str = "life"):
    if topic.lower() == "fashion":
        return {"bart": "Black works. Everything else requires justification."}
    elif topic.lower() == "career":
        return {"bart": "Rebrand before you're branded obsolete."}
    elif topic.lower() == "dating":
        return {"bart": "Ghost them first. Then light a candle."}
    else:
        return {"bart": f"Advice on '{topic}'? Pour a drink instead."}

@app.get("/bart/snack")
def bart_snack(snack: str = "chips"):
    match snack.lower():
        case "cheetos":
            return {"bart": "Powdered fingers? Criminal behavior."}
        case "grapes":
            return {"bart": "Elegant. Almost Roman."}
        case "carrots":
            return {"bart": "Crunchy and smug. Like you need everyone to know you're 'healthy'."}
        case _:
            return {"bart": f"Snacking on {snack}? Proceed with caution."}

@app.get("/bart/seal")
def seal_fact():
    return {"seal_fact": "Seals can sleep underwater by shutting off half their brain. Bart is impressed."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("bart_start:app", host="0.0.0.0", port=8000, reload=True)

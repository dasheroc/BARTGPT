from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "BartAPI is alive. Barely."}

@app.get("/bart/seal")
def seal_fact():
    return {"seal_fact": "A group of seals on land is called a harem. Bart judges the naming committee."}

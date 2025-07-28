from fastapi import FastAPI
from datetime import datetime
import pytz
import random
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)

@app.get("/")
def read_root():
    now = datetime.now(pytz.timezone("America/New_York"))
    return {
        "message": "Hello from BARTAPI!",
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S %Z")
    }

@app.get("/bart/seal")
def seal_fact():
    facts = [
        "Seals can sleep underwater by shutting off half their brain. Bart is impressed.",
        "Some seals can dive over 1,500 feet deep. Bart is impressed.",
        "Seal pups can recognize their mother’s voice just days after birth.",
        "A group of seals on land is called a harem. Bart judges the naming committee.",
        "Seals clap underwater—not to applaud, but to warn rivals. Bart approves."
    ]
    chosen = random.choice(facts)
    logging.info(f"Random fact chosen: {chosen}")
    return {"seal_fact": chosen}
@app.get("/")
def root():
    return {"message": "BartGPT API is alive. Try /docs for the interface."}

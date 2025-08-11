# === BART / FILM MODULE ======================
from typing import List, Optional
from fastapi import Query, HTTPException
import difflib, random

FILM_DB = {
    "suspiria (2018)": {
        "year": 2018,
        "director": "Luca Guadagnino",
        "tagline": "Bodies as percussion. Berlin as séance.",
        "cast": ["Dakota Johnson", "Tilda Swinton", "Mia Goth"],
        "themes": ["power", "ritual", "motherhood", "politics"],
        "plot_min": "An American dancer joins a Berlin academy and discovers it’s a coven. Pirouettes with knives.",
    },
    "fargo (1996)": {
        "year": 1996,
        "director": "Joel Coen",
        "tagline": "Nice folks. Grim decisions. Woodchipper optional.",
        "cast": ["Frances McDormand", "William H. Macy", "Steve Buscemi"],
        "themes": ["greed", "banality of evil", "midwest manners"],
        "plot_min": "A bungled kidnapping unravels in snow and shame. Margie has range.",
    },
    "barry lyndon (1975)": {
        "year": 1975,
        "director": "Stanley Kubrick",
        "tagline": "Candlelit hubris in powdered form.",
        "cast": ["Ryan O'Neal", "Marisa Berenson"],
        "themes": ["class", "fortune", "inevitability"],
        "plot_min": "An ambitious Irishman climbs polite society’s staircase and slips on every step.",
    },
}

SASS = [
    "Correct. Minimal taste detected.",
    "Acceptable. Don’t get cocky.",
    "Bold choice. I’m listening.",
    "Hmm. Courageous… or derivative. We’ll see.",
    "Try that again with a film that owns a spine.",
]

def _canonize(title: str) -> str:
    return title.strip().lower()

def _match_title(title: str) -> Optional[str]:
    key = _canonize(title)
    if key in FILM_DB:
        return key
    # fuzzy suggestion
    choices = list(FILM_DB.keys())
    guess = difflib.get_close_matches(key, choices, n=1, cutoff=0.6)
    return guess[0] if guess else None

@app.get(
    "/bart/film",
    summary="Get Bart’s judgment + film facts",
    description="Supply a film title. Optionally select which fields to return. Fuzzy matches included.",
    tags=["Film"]
)
def film_info(
    title: str,
    fields: List[str] = Query(
        default=["year", "director", "tagline", "plot_min", "themes", "cast"],
        description="Pick fields to include"
    ),
    verbose: bool = False
):
    match = _match_title(title)
    if not match:
        raise HTTPException(
            status_code=404,
            detail=f"No record for '{title}'. Try one of: {sorted(FILM_DB.keys())}"
        )

    data = FILM_DB[match]
    payload = {"title": match.title()}
    for f in fields:
        if f in data:
            payload[f] = data[f]

    # Judgment layer
    verdicts = {
        "suspiria (2018)": "Correct. Bart nods—blood-red approval.",
        "fargo (1996)": "Acceptable. Polite evil, crisp snow, good coat work.",
        "barry lyndon (1975)": "Civilized devastation. You may sit at the adult table.",
    }
    payload["bart_verdict"] = verdicts.get(match, random.choice(SASS))

    if verbose:
        payload["notes"] = "Local DB source. Add OMDb/TMDb later if you insist on homework."

    return payload

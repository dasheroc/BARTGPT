from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random
from typing import Optional

app = FastAPI(title="Sealema API + Bart UI", version="0.2.0")

# ... then FILM_FACTS list, the /api/fact endpoint, the /api/health endpoint, and both UI routes ...

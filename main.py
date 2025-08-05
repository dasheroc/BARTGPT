from flask import Flask, render_template, request
import random
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

film_facts = [
    "Her (2013): A man falls in love with an AI. Curious. But not clever.",
    "The Lobster (2015): Single people are turned into animals. Curious. But not clever.",
    "Synecdoche, New York (2008): A theater director builds a life-size replica of New York inside a warehouse. Curious. But not clever.",
    "The Double Life of Veronique (1991): Two women share a mysterious connection. Curious. But not clever.",
    "Enemy (2013): A man meets his exact double. Curious. But not clever.",
    "Anomalisa (2015): Everyone sounds the same to a lonely man—until one woman doesn’t. Curious. But not clever.",
    "Holy Motors (2012): A man shifts identities across surreal vignettes in a white limo. Curious. But not clever.",
    "There’s Something About Mary (1998): A man meets up with his dream girl from high school, even though his date back then was a complete disaster. Curious. But not clever.",
    "Hello, My Name Is Doris (2015): A self-help seminar inspires a sixty-something woman to romantically pursue her younger co-worker. Curious. But not clever."
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return render_template("chat.html", fact=random.choice(film_facts))
    return render_template("chat.html", fact=random.choice(film_facts))

if __name__ == "__main__":
    app.run(debug=True)

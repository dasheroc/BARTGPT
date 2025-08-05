from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="static")

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

@app.route("/", methods=["GET"])
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"response": "Silence speaks volumes. Try again."})

    if user_input.lower().startswith("film:"):
        title = user_input[5:].strip()
        omdb_response = requests.get(
            f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
        )
        movie_data = omdb_response.json()

        if movie_data.get("Response") == "True":
            description = movie_data.get("Plot", "A mystery untold.")
            response = f'Bart speaks from the abyss: “{movie_data["Title"]} ({movie_data["Year"]}): {description}” — curious. But not clever.'
        else:
            response = 'Bart snarls: “Your so-called *film* eludes even the archive. Try again—with taste.”'
    else:
        response = 'Bart speaks from the abyss: “What time is it?” — curious. But not clever.'

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

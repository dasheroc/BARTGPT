from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

OMDB_API_KEY = os.getenv("OMDB_API_KEY")  # Optional safety fallback

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("input", "").strip()

    if not user_input:
        return jsonify({"response": "Bart stares silently. Try again."})

    try:
        response = requests.get(
            "http://www.omdbapi.com/",
            params={"t": user_input, "apikey": OMDB_API_KEY or "your-default-key"}
        )
        movie = response.json()

        if movie.get("Response") == "True":
            title = movie.get("Title", "Unknown")
            year = movie.get("Year", "Unknown")
            plot = movie.get("Plot", "No plot available.")
            return jsonify({"response": f"🧠 {title} ({year}): {plot}"})
        else:
            return jsonify({"response": f"Bart squints. He’s never heard of '{user_input}'."})
    except Exception as e:
        print("Error in /chat:", e)
        return jsonify({"response": "Bart choked on your input. Try again later."})

if __name__ == "__main__":
    app.run(debug=True)

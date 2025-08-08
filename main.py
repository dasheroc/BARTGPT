from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)
OMDB_API_KEY = os.getenv("OMDB_API_KEY")  # Must be defined in your Render env vars

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_input = data.get("user_input", "").strip()

    if not user_input:
        return jsonify({"response": "Bart stares silently. Try again."})

    # Query OMDb
    try:
        resp = requests.get("http://www.omdbapi.com/", params={
            "t": user_input,
            "apikey": OMDB_API_KEY
        })
        if resp.status_code == 200:
            m = resp.json()
            if m.get("Response") == "True":
                title, year, plot = m.get("Title"), m.get("Year"), m.get("Plot")
                return jsonify({"response": f"{title} ({year}): {plot}"})
            else:
                return jsonify({"response": f"Bart has no record of \"{user_input}\"."})
    except Exception:
        pass

    return jsonify({"response": "Something went wrong—Bart is confounded."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


from flask import Flask, render_template, request, jsonify
import requests
import random
import os

app = Flask(__name__)

# Load OMDB key from environment or hardcode (bad practice, but your call)
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "your_actual_api_key_here")

BART_TONE = 'Bart speaks from the abyss: “{}” — curious. But not clever.'

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/get_movie_fact', methods=['POST'])
def get_movie_fact():
    user_input = request.form['text'].strip()
    if not user_input:
        return jsonify({'fact': "Bart yawns from the void. Say something real."})

    # Query OMDB for movie suggestions
    try:
        response = requests.get(
            "http://www.omdbapi.com/",
            params={"s": user_input, "apikey": OMDB_API_KEY}
        )
        data = response.json()
        if "Search" in data:
            movie = random.choice(data["Search"])
            title = movie.get("Title")
            year = movie.get("Year")

            # Get detailed plot
            details = requests.get(
                "http://www.omdbapi.com/",
                params={"t": title, "y": year, "apikey": OMDB_API_KEY}
            ).json()

            plot = details.get("Plot", "No plot found.")
            if plot != "N/A":
                full_fact = f"{title} ({year}): {plot}"
            else:
                full_fact = f"{title} ({year}): No summary available."
            return jsonify({'fact': BART_TONE.format(full_fact)})
        else:
            return jsonify({'fact': "Bart shrugs. No cinematic match found."})
    except Exception as e:
        return jsonify({'fact': f"Bart grimaces. Something broke: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)

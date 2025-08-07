from flask import Flask, render_template, request, jsonify
import openai
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static')
openai.api_key = os.getenv("OPENAI_API_KEY")
omdb_api_key = os.getenv("OMDB_API_KEY")


@app.route('/')
def index():
    return render_template("chat.html")


@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.get_json()["message"]

        # Try OMDB first if it's a film
        omdb_url = f"http://www.omdbapi.com/?t={user_message}&apikey={omdb_api_key}"
        omdb_response = requests.get(omdb_url).json()

        if omdb_response.get("Response") == "True":
            title = omdb_response.get("Title", "Unknown Title")
            year = omdb_response.get("Year", "N/A")
            plot = omdb_response.get("Plot", "No plot available.")
            return jsonify(response=f"*{title}* ({year}): {plot}")

        # Fallback to GPT if not a valid film
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}],
            temperature=0.7
        )
        reply = completion.choices[0].message.content.strip()
        return jsonify(response=reply)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(response="Bart has laryngitis. Something went wrong."), 500


if __name__ == '__main__':
    app.run(debug=True)

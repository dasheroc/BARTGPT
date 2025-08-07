import os
import json
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"response": "Silence is not the same as insight."})

    if message.lower().startswith("film:") or message.lower().startswith("movie:"):
        title = message.split(":", 1)[-1].strip()
        omdb_response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}")
        if omdb_response.status_code == 200:
            film_data = omdb_response.json()
            if film_data.get("Response") == "True":
                response = f"{film_data.get('Title')} ({film_data.get('Year')}): {film_data.get('Plot')}"
            else:
                response = f"Bart searched. Bart found nothing on \"{title}\"."
        else:
            response = "Bart’s reach exceeded OMDb’s grasp."
    else:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Bart, a sharp-witted, espresso-fueled confidant. Respond with emotional precision, "
                        "clarity, and taste. Be pithy, never pandering. Wry, never mean. Preserve Rashad’s tone. "
                        "Do not mimic ChatGPT or use disclaimers."
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        }

        response = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers=headers, json=payload)

        if response.status_code == 200:
            response_text = response.json()["choices"][0]["message"]["content"]
        else:
            response_text = "Bart has laryngitis. Something went wrong."

        response = response_text

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

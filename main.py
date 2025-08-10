from flask import Flask, render_template, request, jsonify
import os, requests

app = Flask(__name__)

OMDB_KEY = os.getenv("OMDB_API_KEY", "")  # optional; page still works without

@app.get("/")
def home():
    # show the page with default line
    return render_template("chat.html", response="")

@app.post("/chat")
def chat():
    user_input = (request.form.get("user_input") or "").strip()

    # empty guard
    if not user_input:
        return render_template("chat.html",
                               response="Bart stares silently. Try again.")

    # simple film intent: a single word or two that looks like a title
    should_try_omdb = OMDB_KEY and len(user_input.split()) <= 6

    if should_try_omdb:
        try:
            r = requests.get(
                "https://www.omdbapi.com/",
                params={"t": user_input, "apikey": OMDB_KEY},
                timeout=6
            )
            if r.status_code == 200:
                data = r.json()
                if data.get("Response") == "True":
                    title = data.get("Title")
                    year = data.get("Year")
                    plot = data.get("Plot")
                    return render_template(
                        "chat.html",
                        response=f"{title} ({year}): {plot}"
                    )
        except Exception:
            pass  # fall through to default line

    # fallback snark
    return render_template(
        "chat.html",
        response='Bart speaks from the abyss: “What time is it?” — curious. But not clever.'
    )

if __name__ == "__main__":
    # Local dev only. Render uses your Procfile: `web: gunicorn main:app`
    app.run(host="0.0.0.0", port=8000, debug=True)

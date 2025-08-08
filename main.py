from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = request.form["user_input"]

        # You can swap this block with your own logic
        url = f"http://www.omdbapi.com/?t={user_input}&apikey=YOUR_OMDB_API_KEY"
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                m = resp.json()
                if m.get("Response") == "True":
                    title = m.get("Title")
                    year = m.get("Year")
                    plot = m.get("Plot")
                    return render_template("chat.html", response=f"{title} ({year}): {plot}")
                else:
                    return render_template("chat.html", response=f"Bart has no record of “{user_input}”.")
        except Exception:
            pass

        return render_template("chat.html", response="Something went wrong—Bart is confounded.")

    return render_template("chat.html")

if __name__ == "__main__":
    app.run(debug=True)

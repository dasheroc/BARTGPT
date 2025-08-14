from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def get_chat():
    if request.method == "POST":
        title = request.form.get("title", "").lower()
    else:
        title = request.args.get("title", "").lower()

    judgment = ""

    match title:
        case "suspiria":
            judgment = "Correct. Bart nods."
        case "fargo":
            judgment = "Acceptable. Bart squints."
        case "barbie":
            judgment = "Chaotic glitter. Bart smirks."
        case "oppenheimer":
            judgment = "Boom. Bart contemplates existence."
        case "gone girl":
            judgment = "Cool Girl. Bart conforms to toxic masculinity."
        case "possession":
            judgment = "Cosmic Horror. Bart is unhinged and melting dramatically."
        case _:
            judgment = "Wrong. Bart sighs."

    return render_template("chat.html", judgment=judgment)


if __name__ == "__main__":
    app.run(debug=True)

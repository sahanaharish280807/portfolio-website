from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.get_json().get("message").lower()

    if "project" in msg:
        reply = "I built a Notes App, Expense Tracker, and Portfolio website."
    elif "skill" in msg:
        reply = "I work with Python, Flask, HTML, CSS, and JavaScript."
    else:
        reply = "Hi! I'm Sahana 👋 Ask me about my projects or skills!"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
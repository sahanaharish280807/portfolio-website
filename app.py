from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message").lower()

    if "project" in msg:
        reply = "I built a Notes App, Expense Tracker, and Portfolio Website."
    elif "skill" in msg:
        reply = "My skills include Python, Flask, HTML, CSS, and JavaScript."
    elif "about" in msg:
        reply = "I'm Sahana Harish, a Full Stack Developer who loves clean UI and web apps."
    else:
        reply = "Hi! I'm Sahana Harish 💖 Ask me about my projects or skills!"

    return jsonify({"reply": reply})

    if __name__ == "__main__":
        app.run(debug=True)
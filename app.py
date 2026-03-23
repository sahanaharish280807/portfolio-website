from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.get_json().get("message").lower()

    if "project" in msg:
        reply = "I built a Notes App, Expense Tracker, and a Portfolio Website."
    elif "skill" in msg:
        reply = "My skills include Python, Flask, HTML, CSS, and JavaScript."
    elif "about" in msg:
        reply = "I'm Sahana, a passionate Full Stack Developer who enjoys building clean and interactive applications."
    else:
        reply = "Hi! I'm Sahana 👋 Ask me about my skills, projects, or experience!"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
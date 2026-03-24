from flask import Flask, render_template, request, jsonify
import traceback

app = Flask(__name__)

@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception as e:
        return f"Error loading template: {e}<br>Check that templates/index.html exists"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        msg = request.json.get("message").lower()
        print(f"Received message: {msg}")  # This will show in terminal

        if "project" in msg:
            reply = "I built a Notes App, Expense Tracker, and Portfolio Website."
        elif "skill" in msg:
            reply = "My skills include Python, Flask, HTML, CSS, and JavaScript."
        elif "about" in msg:
            reply = "I'm Sahana, a Full Stack Developer who loves clean UI and web apps."
        else:
            reply = "Hi! I'm Sahana 💖 Ask me about my projects or skills!"

        return jsonify({"reply": reply})
    except Exception as e:
        print(f"Error in chat: {e}")
        traceback.print_exc()
        return jsonify({"reply": f"Error: {str(e)}"})
    
@app.route("/contact", methods=["POST"])
def contact():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    subject = data.get("subject")
    message = data.get("message")
    
    # Print to console (you can save to database or send email)
    print(f"New message from {name} ({email}): {subject} - {message}")
    
    return jsonify({"status": "success", "message": "Message received!"})    

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
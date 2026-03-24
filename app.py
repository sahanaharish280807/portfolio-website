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
    
 @app.route("/view-data")
def view_data():
    chat_content = ""
    contact_content = ""
    
    if os.path.exists("chat_log.txt"):
        with open("chat_log.txt", "r") as f:
            chat_content = f.read()
    
    if os.path.exists("contact_data.txt"):
        with open("contact_data.txt", "r") as f:
            contact_content = f.read()
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>View Data</title>
        <style>
            body {{ font-family: Arial; padding: 20px; background: #f5f5f5; }}
            .section {{ background: white; padding: 20px; margin: 20px 0; border-radius: 10px; }}
            h2 {{ color: #667eea; }}
            pre {{ background: #f0f0f0; padding: 15px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <h1>📊 Portfolio Data</h1>
        <div class="section">
            <h2>💬 Chat Messages</h2>
            <pre>{chat_content or "No messages yet"}</pre>
        </div>
        <div class="section">
            <h2>📧 Contact Form</h2>
            <pre>{contact_content or "No messages yet"}</pre>
        </div>
        <a href="/">← Back</a>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

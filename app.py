from flask import Flask, render_template, request, jsonify
import traceback
import os

app = Flask(__name__)

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception as e:
        return f"Error loading template: {e}<br>Check templates/index.html exists"


# ---------------- CHAT BOT ----------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        msg = request.json.get("message").lower()
        print(f"Received message: {msg}")

        # ✅ Save chat message
        with open("chat_log.txt", "a") as f:
            f.write(msg + "\n")

        if "project" in msg:
            reply = "I built a Notes App, Expense Tracker, and Portfolio Website."
        elif "skill" in msg:
            reply = "My skills include Python, Flask, HTML, CSS, and JavaScript."
        elif "about" in msg:
            reply = "I'm Sahana, a Full Stack Developer who loves clean UI and web apps."
        else:
            reply = "Hi! I'm Sahana ❤️ Ask me about my projects or skills!"

        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Error in chat: {e}")
        traceback.print_exc()
        return jsonify({"reply": f"Error: {str(e)}"})


# ---------------- CONTACT FORM ----------------
@app.route("/contact", methods=["POST"])
def contact():
    try:
        data = request.json

        name = data.get("name")
        email = data.get("email")
        subject = data.get("subject")
        message = data.get("message")

        # ✅ Save contact data
        with open("contact_data.txt", "a") as f:
            f.write(f"{name}, {email}, {subject}, {message}\n")

        print(f"New message from {name} ({email}): {subject} - {message}")

        return jsonify({"status": "success", "message": "Message received!"})

    except Exception as e:
        print(f"Error in contact: {e}")
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)})


# ---------------- VIEW DATA PAGE ----------------
@app.route("/view-data")
def view_data():
    chat_content = ""
    contact_content = ""

    # Read chat data
    if os.path.exists("chat_log.txt"):
        with open("chat_log.txt", "r") as f:
            chat_content = f.read()

    # Read contact data
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
            <h2>📩 Contact Form</h2>
            <pre>{contact_content or "No messages yet"}</pre>
        </div>
    </body>
    </html>
    """
@app.route('/data')
def show_data():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacts")
    data = cursor.fetchall()

    conn.close()
    return str(data)

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
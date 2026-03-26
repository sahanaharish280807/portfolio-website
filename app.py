from flask import Flask, render_template, request, jsonify
import traceback
import sqlite3
import os

app = Flask(__name__)

# ---------------- DATABASE INITIALIZATION ----------------
def init_db():
    """Create database and tables if they don't exist"""
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        # Create contacts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create chat_messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")

# Initialize database when app starts
init_db()

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception as e:
        return f"Error loading template: {e}<br>Check that templates/index.html exists"

# ---------------- CHAT BOT ----------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"reply": "Please send a valid message"}), 400
            
        msg = data.get("message").lower()
        print(f"Received message: {msg}")

        # Save chat message to database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chat_messages (message) VALUES (?)", (msg,))
        conn.commit()
        conn.close()

        # Generate response
        if "project" in msg:
            reply = "I built a Notes App, Expense Tracker, and Portfolio Website."
        elif "skill" in msg:
            reply = "My skills include Python, Flask, HTML, CSS, and JavaScript."
        elif "about" in msg:
            reply = "I'm Sahana, a Full Stack Developer who loves clean UI and web apps."
        elif "hello" in msg or "hi" in msg:
            reply = "Hi! I'm Sahana ❤️ Ask me about my projects or skills!"
        else:
            reply = "Hi! I'm Sahana ❤️ Ask me about my projects or skills!"

        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Error in chat: {e}")
        traceback.print_exc()
        return jsonify({"reply": f"Sorry, an error occurred. Please try again."}), 500

# ---------------- CONTACT FORM ----------------
@app.route("/contact", methods=["POST"])
def contact():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400

        name = data.get("name")
        email = data.get("email")
        subject = data.get("subject", "")  # Optional field
        message = data.get("message")

        # Validate required fields
        if not name or not email or not message:
            return jsonify({"status": "error", "message": "Name, email, and message are required"}), 400

        # Save contact data to database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contacts (name, email, subject, message) VALUES (?, ?, ?, ?)",
            (name, email, subject, message)
        )
        conn.commit()
        conn.close()

        print(f"New message from {name} ({email}): {subject} - {message}")

        return jsonify({"status": "success", "message": "Message received successfully!"})

    except Exception as e:
        print(f"Error in contact: {e}")
        traceback.print_exc()
        return jsonify({"status": "error", "message": "Failed to save message. Please try again."}), 500

# ---------------- VIEW DATA PAGE ----------------
@app.route("/view-data")
def view_data():
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        # Fetch chat messages
        cursor.execute("SELECT id, message, created_at FROM chat_messages ORDER BY created_at DESC")
        chat_messages = cursor.fetchall()
        
        # Fetch contact messages
        cursor.execute("SELECT id, name, email, subject, message, created_at FROM contacts ORDER BY created_at DESC")
        contacts = cursor.fetchall()
        
        conn.close()
        
        # Format the data for display
        if chat_messages:
            chat_content = "\n".join([f"[{msg[2]}] {msg[1]}" for msg in chat_messages])
        else:
            chat_content = "No messages yet"
        
        if contacts:
            contact_content = "\n".join([
                f"[{c[5]}] {c[1]} ({c[2]}): {c[3] if c[3] else 'No subject'} - {c[4]}" 
                for c in contacts
            ])
        else:
            contact_content = "No messages yet"
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>View Data - Portfolio Dashboard</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                }}
                h1 {{
                    color: white;
                    text-align: center;
                    margin-bottom: 30px;
                    font-size: 2.5em;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
                }}
                .section {{
                    background: white;
                    padding: 25px;
                    margin: 20px 0;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                }}
                h2 {{
                    color: #667eea;
                    margin-bottom: 15px;
                    border-bottom: 2px solid #667eea;
                    padding-bottom: 10px;
                }}
                .stats {{
                    background: #f0f0f0;
                    padding: 10px;
                    border-radius: 8px;
                    margin-bottom: 15px;
                    font-weight: bold;
                    color: #555;
                }}
                pre {{
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 8px;
                    overflow-x: auto;
                    font-family: 'Courier New', monospace;
                    font-size: 14px;
                    border: 1px solid #e0e0e0;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }}
                .nav {{
                    text-align: center;
                    margin-top: 20px;
                }}
                .nav a {{
                    color: white;
                    text-decoration: none;
                    background: rgba(255,255,255,0.2);
                    padding: 10px 20px;
                    border-radius: 8px;
                    margin: 0 10px;
                    transition: all 0.3s;
                }}
                .nav a:hover {{
                    background: rgba(255,255,255,0.3);
                }}
                .timestamp {{
                    color: #888;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Portfolio Data Dashboard</h1>

                <div class="section">
                    <h2>💬 Chat Messages</h2>
                    <div class="stats">Total messages: {len(chat_messages)}</div>
                    <pre>{chat_content}</pre>
                </div>

                <div class="section">
                    <h2>📩 Contact Form Submissions</h2>
                    <div class="stats">Total submissions: {len(contacts)}</div>
                    <pre>{contact_content}</pre>
                </div>
                
                <div class="nav">
                    <a href="/">🏠 Back to Home</a>
                </div>
            </div>
        </body>
        </html>
        """
    except Exception as e:
        print(f"Error in view-data: {e}")
        traceback.print_exc()
        return f"Error loading data: {str(e)}", 500

# ---------------- API ENDPOINT FOR CONTACTS ----------------
@app.route('/api/contacts')
def get_contacts():
    """API endpoint to get all contacts as JSON"""
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, email, subject, message, created_at FROM contacts ORDER BY created_at DESC")
        contacts = cursor.fetchall()
        
        conn.close()
        
        # Convert to list of dictionaries
        contacts_list = [
            {
                "id": c[0],
                "name": c[1],
                "email": c[2],
                "subject": c[3] if c[3] else "",
                "message": c[4],
                "created_at": c[5]
            }
            for c in contacts
        ]
        
        return jsonify({"status": "success", "data": contacts_list})
    except Exception as e:
        print(f"Error in api/contacts: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------- API ENDPOINT FOR CHAT MESSAGES ----------------
@app.route('/api/chat-messages')
def get_chat_messages():
    """API endpoint to get all chat messages as JSON"""
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, message, created_at FROM chat_messages ORDER BY created_at DESC")
        messages = cursor.fetchall()
        
        conn.close()
        
        # Convert to list of dictionaries
        messages_list = [
            {
                "id": m[0],
                "message": m[1],
                "created_at": m[2]
            }
            for m in messages
        ]
        
        return jsonify({"status": "success", "data": messages_list})
    except Exception as e:
        print(f"Error in api/chat-messages: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
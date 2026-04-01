from flask import Flask, render_template, request, jsonify, redirect, url_for, render_template_string
import traceback
import sqlite3
import os
from flask_mail import Mail, Message

app = Flask(__name__)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sanuharish007@gmail.com'
app.config['MAIL_PASSWORD'] = 'feww ceob efsb vlsf'  # IMPORTANT: Change this to use environment variables in production

mail = Mail(app)

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
        return True
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        return False

# Initialize database when app starts
init_db()

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Portfolio - Home</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding: 50px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }}
                .error-box {{
                    background: rgba(255,255,255,0.9);
                    color: #333;
                    padding: 20px;
                    border-radius: 10px;
                    max-width: 600px;
                    margin: 0 auto;
                }}
                a {{
                    color: #667eea;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="error-box">
                <h1>⚠️ Template Not Found</h1>
                <p>Error loading index.html template: {e}</p>
                <p>Make sure templates/index.html exists in your project folder.</p>
                <hr>
                <h3>Available Pages:</h3>
                <p><a href="/admin">📊 Admin Dashboard</a></p>
                <p><a href="/view-data">📝 View Data</a></p>
                <p><a href="/debug/all">🔧 Debug Info</a></p>
            </div>
        </body>
        </html>
        """

# ---------------- CHAT BOT (CREATE) ----------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"reply": "Please send a valid message"}), 400
            
        msg = data.get("message").lower()
        print(f"Received message: {msg}")

        # CREATE: Save chat message to database
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

# ---------------- CONTACT FORM (CREATE) ----------------
@app.route("/contact", methods=["POST"])
def contact():
    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        subject = data.get("subject", "New Message")
        message = data.get("message")

        if not name or not email or not message:
            return jsonify({"status": "error", "message": "All fields required"}), 400

        # Save to Database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contacts (name, email, subject, message) VALUES (?, ?, ?, ?)",
            (name, email, subject, message)
        )
        conn.commit()
        contact_id = cursor.lastrowid
        conn.close()

        # Send Email (with error handling so form doesn't fail if email fails)
        email_status = "Not attempted"
        try:
            msg = Message(
                subject=f"Portfolio Message: {subject}",
                sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['MAIL_USERNAME']]
            )
            msg.body = f"""
New Contact Message (ID: {contact_id})

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

Submitted at: {request.headers.get('User-Agent', 'Unknown')}
            """
            mail.send(msg)
            email_status = "Email sent successfully"
            print(f"✅ Email sent for contact ID: {contact_id}")
        except Exception as email_err:
            print(f"⚠️ Email error: {email_err}")
            email_status = f"Email failed: {str(email_err)}"

        return jsonify({
            "status": "success", 
            "message": "Message saved successfully!",
            "email_status": email_status,
            "contact_id": contact_id
        })

    except Exception as e:
        print(f"Error in contact: {e}")
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------- READ ALL DATA (Admin Dashboard) ----------------
@app.route("/admin")
def admin_dashboard():
    """Admin dashboard with full CRUD interface"""
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        # READ: Fetch all contacts
        cursor.execute("SELECT * FROM contacts ORDER BY created_at DESC")
        contacts = cursor.fetchall()
        
        # READ: Fetch all chat messages
        cursor.execute("SELECT * FROM chat_messages ORDER BY created_at DESC")
        chats = cursor.fetchall()
        
        conn.close()
        
        return render_template_string(ADMIN_TEMPLATE, contacts=contacts, chats=chats)
    except Exception as e:
        return f"Error: {e}"

# ---------------- UPDATE Contact Message ----------------
@app.route("/admin/contact/update/<int:id>", methods=["POST"])
def update_contact(id):
    try:
        data = request.get_json()
        
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        # UPDATE: Modify contact message
        cursor.execute(
            "UPDATE contacts SET name=?, email=?, subject=?, message=? WHERE id=?",
            (data['name'], data['email'], data['subject'], data['message'], id)
        )
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "Contact updated successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------- DELETE Contact Message ----------------
@app.route("/admin/contact/delete/<int:id>", methods=["DELETE"])
def delete_contact(id):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        # DELETE: Remove contact message
        cursor.execute("DELETE FROM contacts WHERE id=?", (id,))
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "Contact deleted successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------- UPDATE Chat Message ----------------
@app.route("/admin/chat/update/<int:id>", methods=["POST"])
def update_chat(id):
    try:
        data = request.get_json()
        
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        # UPDATE: Modify chat message
        cursor.execute(
            "UPDATE chat_messages SET message=? WHERE id=?",
            (data['message'], id)
        )
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "Chat message updated successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------- DELETE Chat Message ----------------
@app.route("/admin/chat/delete/<int:id>", methods=["DELETE"])
def delete_chat(id):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        # DELETE: Remove chat message
        cursor.execute("DELETE FROM chat_messages WHERE id=?", (id,))
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "Chat message deleted successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------- VIEW DATA PAGE (Simple Read) ----------------
@app.route("/view-data")
def view_data():
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        # READ: Fetch chat messages
        cursor.execute("SELECT id, message, created_at FROM chat_messages ORDER BY created_at DESC")
        chat_messages = cursor.fetchall()
        
        # READ: Fetch contact messages
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
                    <a href="/admin">🔧 Admin Panel (CRUD)</a>
                </div>
            </div>
        </body>
        </html>
        """
    except Exception as e:
        print(f"Error in view-data: {e}")
        traceback.print_exc()
        return f"Error loading data: {str(e)}", 500

# ---------------- API ENDPOINTS FOR CRUD ----------------
@app.route('/api/contacts')
def get_contacts():
    """READ: API endpoint to get all contacts as JSON"""
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, email, subject, message, created_at FROM contacts ORDER BY created_at DESC")
        contacts = cursor.fetchall()
        
        conn.close()
        
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
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/chat-messages')
def get_chat_messages():
    """READ: API endpoint to get all chat messages as JSON"""
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, message, created_at FROM chat_messages ORDER BY created_at DESC")
        messages = cursor.fetchall()
        
        conn.close()
        
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
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------- DEBUG ROUTES ----------------
@app.route("/debug/all")
def debug_all():
    """Comprehensive debug information"""
    import os
    import datetime
    
    debug_info = []
    
    debug_info.append("<!DOCTYPE html><html><head><title>Debug Info</title><style>body{font-family:monospace;padding:20px;background:#f5f5f5;} .section{background:white;padding:15px;margin:10px 0;border-radius:5px;}</style></head><body>")
    debug_info.append("<h1>🔧 Debug Information</h1>")
    
    # 1. Check database
    debug_info.append("<div class='section'><h2>📁 Database Status:</h2>")
    if os.path.exists("database.db"):
        size = os.path.getsize("database.db")
        modified = datetime.datetime.fromtimestamp(os.path.getmtime("database.db"))
        debug_info.append(f"✅ Database exists: {size} bytes")
        debug_info.append(f"📅 Last modified: {modified}")
        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM contacts")
            count = cursor.fetchone()[0]
            debug_info.append(f"✅ Contacts count: {count}")
            
            cursor.execute("SELECT COUNT(*) FROM chat_messages")
            chat_count = cursor.fetchone()[0]
            debug_info.append(f"✅ Chat messages count: {chat_count}")
            
            if count > 0:
                cursor.execute("SELECT * FROM contacts ORDER BY id DESC LIMIT 3")
                recent = cursor.fetchall()
                debug_info.append("<br><b>Recent 3 submissions:</b><br>")
                for r in recent:
                    debug_info.append(f"  - ID: {r[0]}, Name: {r[1]}, Created: {r[5]}<br>")
            conn.close()
        except Exception as e:
            debug_info.append(f"❌ Database error: {e}")
    else:
        debug_info.append("❌ No database file found!")
    debug_info.append("</div>")
    
    # 2. Check email config
    debug_info.append("<div class='section'><h2>📧 Email Status:</h2>")
    debug_info.append(f"MAIL_SERVER: {app.config.get('MAIL_SERVER')}<br>")
    debug_info.append(f"MAIL_PORT: {app.config.get('MAIL_PORT')}<br>")
    debug_info.append(f"MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}<br>")
    debug_info.append(f"MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}<br>")
    debug_info.append(f"MAIL_PASSWORD: {'*' * len(str(app.config.get('MAIL_PASSWORD', ''))) if app.config.get('MAIL_PASSWORD') else 'NOT SET'}<br>")
    debug_info.append("</div>")
    
    # 3. Server info
    debug_info.append("<div class='section'><h2>🖥️ Server Info:</h2>")
    debug_info.append(f"Running on: {request.host}<br>")
    debug_info.append(f"Debug mode: {app.debug}<br>")
    debug_info.append(f"Python version: {os.sys.version}<br>")
    debug_info.append("</div>")
    
    # 4. Available routes
    debug_info.append("<div class='section'><h2>🔗 Available Routes:</h2>")
    debug_info.append("<ul>")
    debug_info.append("<li><a href='/'>🏠 Home</a></li>")
    debug_info.append("<li><a href='/admin'>🔧 Admin Panel</a></li>")
    debug_info.append("<li><a href='/view-data'>📊 View Data</a></li>")
    debug_info.append("<li><a href='/api/contacts'>📡 API: Contacts</a></li>")
    debug_info.append("<li><a href='/api/chat-messages'>📡 API: Chat Messages</a></li>")
    debug_info.append("</ul>")
    debug_info.append("</div>")
    
    debug_info.append("</body></html>")
    
    return "".join(debug_info)

@app.route("/debug/test-email")
def test_email():
    """Test email sending"""
    try:
        msg = Message(
            subject="Test Email from Flask Portfolio",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']]
        )
        msg.body = f"""
Test Email

This is a test email sent from your Flask application at {datetime.datetime.now()}

If you received this, email is working correctly!
        """
        mail.send(msg)
        return """
        <!DOCTYPE html>
        <html>
        <head><title>Email Test</title></head>
        <body style="font-family: Arial; padding: 20px;">
            <h1 style="color: green;">✅ Email Sent Successfully!</h1>
            <p>Check your inbox/spam folder at: {}</p>
            <hr>
            <a href="/debug/all">Back to Debug</a>
        </body>
        </html>
        """.format(app.config['MAIL_USERNAME'])
    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>Email Test Failed</title></head>
        <body style="font-family: Arial; padding: 20px;">
            <h1 style="color: red;">❌ Email Failed</h1>
            <p><strong>Error:</strong> {str(e)}</p>
            <hr>
            <a href="/debug/all">Back to Debug</a>
        </body>
        </html>
        """

# ---------------- ADMIN TEMPLATE (HTML with CRUD Interface) ----------------
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel - CRUD Operations</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
        }
        .section {
            background: white;
            padding: 25px;
            margin-bottom: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .section h2 {
            color: #667eea;
            margin-bottom: 20px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        th {
            background: #f8f9fa;
            font-weight: bold;
            color: #555;
        }
        tr:hover {
            background: #f8f9fa;
        }
        .btn {
            padding: 5px 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 0 3px;
            font-size: 12px;
        }
        .btn-edit {
            background: #4caf50;
            color: white;
        }
        .btn-delete {
            background: #f44336;
            color: white;
        }
        .btn-save {
            background: #2196f3;
            color: white;
        }
        .btn-cancel {
            background: #9e9e9e;
            color: white;
        }
        .edit-form input, .edit-form textarea {
            width: 100%;
            padding: 8px;
            margin: 5px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-family: inherit;
        }
        .edit-form textarea {
            resize: vertical;
        }
        .nav {
            margin-top: 20px;
            text-align: center;
        }
        .nav a {
            color: #667eea;
            text-decoration: none;
            margin: 0 10px;
        }
        .stats {
            background: #e3f2fd;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        .empty-message {
            text-align: center;
            color: #999;
            padding: 40px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 Admin Panel - CRUD Operations</h1>
        <p class="subtitle">Create, Read, Update, Delete operations for your portfolio data</p>
        
        <div class="section">
            <h2>📩 Contact Form Submissions</h2>
            <div class="stats">Total: {{ contacts|length }} messages</div>
            {% if contacts %}
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Subject</th>
                        <th>Message</th>
                        <th>Created</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for contact in contacts %}
                    <tr id="contact-row-{{ contact[0] }}">
                        <td>{{ contact[0] }}</td>
                        <td class="name-{{ contact[0] }}">{{ contact[1] }}</td>
                        <td class="email-{{ contact[0] }}">{{ contact[2] }}</td>
                        <td class="subject-{{ contact[0] }}">{{ contact[3] or '-' }}</td>
                        <td class="message-{{ contact[0] }}">{{ contact[4] }}</td>
                        <td>{{ contact[5] }}</td>
                        <td>
                            <button class="btn btn-edit" onclick="editContact({{ contact[0] }})">Edit</button>
                            <button class="btn btn-delete" onclick="deleteContact({{ contact[0] }})">Delete</button>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="empty-message">No contact form submissions yet.</div>
            {% endif %}
        </div>
        
        <div class="section">
            <h2>💬 Chat Messages</h2>
            <div class="stats">Total: {{ chats|length }} messages</div>
            {% if chats %}
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Message</th>
                        <th>Created</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for chat in chats %}
                    <tr id="chat-row-{{ chat[0] }}">
                        <td>{{ chat[0] }}</td>
                        <td class="chat-msg-{{ chat[0] }}">{{ chat[1] }}</td>
                        <td>{{ chat[2] }}</td>
                        <td>
                            <button class="btn btn-edit" onclick="editChat({{ chat[0] }})">Edit</button>
                            <button class="btn btn-delete" onclick="deleteChat({{ chat[0] }})">Delete</button>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="empty-message">No chat messages yet.</div>
            {% endif %}
        </div>
        
        <div class="nav">
            <a href="/">🏠 Home</a> | 
            <a href="/view-data">📊 View Data</a> |
            <a href="/debug/all">🔧 Debug</a>
        </div>
    </div>
    
    <script>
        function editContact(id) {
            const name = document.querySelector(`.name-${id}`).innerText;
            const email = document.querySelector(`.email-${id}`).innerText;
            const subject = document.querySelector(`.subject-${id}`).innerText;
            const message = document.querySelector(`.message-${id}`).innerText;
            
            const newName = prompt("Edit name:", name);
            if (newName === null) return;
            const newEmail = prompt("Edit email:", email);
            if (newEmail === null) return;
            const newSubject = prompt("Edit subject:", subject === '-' ? '' : subject);
            if (newSubject === null) return;
            const newMessage = prompt("Edit message:", message);
            if (newMessage === null) return;
            
            fetch(`/admin/contact/update/${id}`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    name: newName,
                    email: newEmail,
                    subject: newSubject,
                    message: newMessage
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Contact updated successfully!');
                    location.reload();
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                alert('Error: ' + error);
            });
        }
        
        function deleteContact(id) {
            if (confirm('Are you sure you want to delete this contact message?')) {
                fetch(`/admin/contact/delete/${id}`, {
                    method: 'DELETE'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('Contact deleted successfully!');
                        location.reload();
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch(error => {
                    alert('Error: ' + error);
                });
            }
        }
        
        function editChat(id) {
            const message = document.querySelector(`.chat-msg-${id}`).innerText;
            const newMessage = prompt("Edit message:", message);
            
            if (newMessage === null) return;
            
            fetch(`/admin/chat/update/${id}`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: newMessage})
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Chat message updated successfully!');
                    location.reload();
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                alert('Error: ' + error);
            });
        }
        
        function deleteChat(id) {
            if (confirm('Are you sure you want to delete this chat message?')) {
                fetch(`/admin/chat/delete/${id}`, {
                    method: 'DELETE'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('Chat message deleted successfully!');
                        location.reload();
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch(error => {
                    alert('Error: ' + error);
                });
            }
        }
    </script>
</body>
</html>
"""

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    # Run the app
    app.run(debug=True, host='127.0.0.1', port=5000)

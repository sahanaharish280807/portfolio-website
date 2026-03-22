from flask import Flask, request, jsonify, render_template
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

def init_db():
    """Initialize the database with proper table structure"""
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.close()
    print("Database initialized successfully!")

@app.route('/')
def home():
    """Render the homepage"""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Handle contact form submission"""
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        
        # Validate input
        if not name or not email or not message:
            return jsonify({
                'success': False,
                'message': 'Please fill in all fields'
            }), 400
        
        # Validate email format
        if '@' not in email or '.' not in email:
            return jsonify({
                'success': False,
                'message': 'Please enter a valid email address'
            }), 400
        
        # Save to database
        conn = sqlite3.connect('database.db')
        conn.execute(
            "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Thank you {name}! Your message has been sent successfully.'
        })
        
    except Exception as e:
        print(f"Error: {e}")  # This will appear in PythonAnywhere logs
        return jsonify({
            'success': False,
            'message': 'An error occurred. Please try again later.'
        }), 500

@app.route('/view-messages')
def view_messages():
    """View all messages (protected - you might want to add authentication)"""
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.execute("SELECT id, name, email, message, created_at FROM contacts ORDER BY created_at DESC")
        messages = cursor.fetchall()
        conn.close()
        
        if not messages:
            return "<h1>No messages yet</h1><a href='/'>Back to Home</a>"
        
        html = "<h1>Contact Messages</h1>"
        html += "<a href='/'>← Back to Home</a><br><br>"
        html += "<table border='1' cellpadding='10' style='border-collapse: collapse;'>"
        html += "<tr><th>ID</th><th>Name</th><th>Email</th><th>Message</th><th>Date</th></tr>"
        
        for msg in messages:
            html += f"<tr>"
            html += f"<td>{msg[0]}</td>"
            html += f"<td>{msg[1]}</td>"
            html += f"<td>{msg[2]}</td>"
            html += f"<td>{msg[3]}</td>"
            html += f"<td>{msg[4]}</td>"
            html += f"</tr>"
        
        html += "</table>"
        return html
        
    except Exception as e:
        return f"Error: {e}"

# For local development
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT',10000)))

# For PythonAnywhere
application = app
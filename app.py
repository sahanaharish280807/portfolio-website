from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)

# Use /tmp for database on Render
DATABASE_PATH = '/tmp/database.db'

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute('CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, message TEXT)')
    conn.close()

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    message = request.form.get('message', '')
    
    if not name or not email or not message:
        return "Please fill all fields", 400
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
                   (name, email, message))
    conn.commit()
    conn.close()
    
    return "Message Stored Successfully!"

@app.route('/view')
def view():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.execute("SELECT * FROM contacts")
    
    data = "<h1>Messages</h1><a href='/'>Back</a><br><br>"
    for row in cursor:
        data += f"Name: {row[1]}, Email: {row[2]}, Message: {row[3]}<br>"
    
    conn.close()
    return data

@app.route('/view-data')
def view_data():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.execute("SELECT * FROM contacts")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/')
def home():
    return render_template('index.html')

# Initialize database
init_db()

# For Render
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

application = app
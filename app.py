from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name TEXT, email TEXT, message TEXT)')
    conn.commit()
    conn.close()

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", 
                 (name, email, message))
    conn.commit()
    conn.close()

    return "Message Stored Successfully!"

@app.route('/view')
def view():
    conn = sqlite3.connect('database.db')
    cursor = conn.execute("SELECT * FROM contacts")

    data = ""
    for row in cursor:
        data += f"Name: {row[0]}, Email: {row[1]}, Message: {row[2]}<br>"

    conn.close()
    return data

@app.route('/view-data')
def view_data():
    conn = sqlite3.connnect('database.db')
    cursor = conn.execute("SELECT * FROM contacts")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
application = app
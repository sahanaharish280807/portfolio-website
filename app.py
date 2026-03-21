from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name TEXT, email TEXT, message TEXT)')
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

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
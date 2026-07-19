from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# डेटाबेस कन्फिगरेसन
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# सुरुमा टेबल बनाउने
conn = get_db_connection()
conn.execute('CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, date TEXT, rank TEXT, name TEXT, remarks TEXT)')
conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form.get('date') 
        rank = request.form.get('rank')
        name = request.form.get('name')
        remarks = request.form.get('remarks')
        
        conn = get_db_connection()
        conn.execute('INSERT INTO entries (date, rank, name, remarks) VALUES (?, ?, ?, ?)', (date, rank, name, remarks))
        conn.commit()
        conn.close()
        return redirect('/dashboard')
    return render_template('form.html')

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    entries = conn.execute('SELECT * FROM entries').fetchall()
    conn.close()
    return render_template('dashboard.html', entries=entries)

if __name__ == '__main__':
    app.run()
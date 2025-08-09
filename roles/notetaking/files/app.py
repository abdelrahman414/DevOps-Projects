from flask import Flask, request, redirect, render_template, url_for, flash
import sqlite3
from datetime import datetime
import os

DB_PATH = '/srv/notetaking/notes.db'
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "supersecretkey"  # Needed for flash messages

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE notes (id INTEGER PRIMARY KEY, content TEXT, created_at TEXT)''')
        conn.commit()
        conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if request.method == 'POST':
        note = request.form.get('note')
        if note.strip():
            c.execute('INSERT INTO notes (content, created_at) VALUES (?, ?)',
                      (note.strip(), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            flash("Note added successfully!", "success")
        else:
            flash("Note cannot be empty!", "error")
    c.execute('SELECT * FROM notes ORDER BY created_at DESC')
    notes = c.fetchall()
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/delete/<int:note_id>', methods=['POST'])
def delete(note_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM notes WHERE id=?', (note_id,))
    conn.commit()
    conn.close()
    flash("Note deleted!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000)

import sqlite3
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

DATABASE = 'notes.db'

# Sukuria duomenų bazės prisijungimą


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Sukuria lentelę, jei ji dar neegzistuoja


def create_tables():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            note TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()


create_tables()  # Užtikrina, kad lentelės būtų sukurtos prieš pradedant programą

# Pagrindinis puslapis, kuris rodo užrašus ir leidžia juos įvesti


@app.route('/', methods=['GET', 'POST'])
def notebook():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form.get('vardas')
        note = request.form.get('uzrasas')
        if name and note:
            conn.execute(
                'INSERT INTO notes (name, note) VALUES (?, ?)', (name, note))
            conn.commit()
        return redirect(url_for('notebook'))

    notes = conn.execute('SELECT name, note FROM notes').fetchall()
    conn.close()
    return render_template('uzrasine.html', uzrasai=notes)

# Archyvo puslapis, kuris rodo visus užrašus, išrikiuotus pagal vardą


@app.route('/archyvas', methods=['GET', 'POST'])
def archyvas():
    if request.method == 'POST':
        return redirect(url_for('notebook'))

    conn = get_db_connection()
    notes = conn.execute(
        'SELECT name, note FROM notes ORDER BY name').fetchall()
    conn.close()
    return render_template('archyvas.html', uzrasai=notes)


@app.route('/user/<username>', methods=['GET'])
def user_notes(username):
    conn = get_db_connection()
    user_notes = conn.execute(
        'SELECT name, note FROM notes WHERE name = ?', (username,)
    ).fetchall()
    conn.close()
    return render_template('user_notes.html', username=username, notes=user_notes)


if __name__ == '__main__':
    app.run(debug=True)  # Paleidžia programą su įjungtu klaidų ieškojimo režimu

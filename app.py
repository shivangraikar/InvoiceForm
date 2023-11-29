from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# SQLite database setup
conn = sqlite3.connect('forms.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS forms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        invoice TEXT NOT NULL,
        job TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        company = request.form['company']
        invoice = request.form['invoice']
        job = request.form['job']

        # Store data in the database
        conn = sqlite3.connect('forms.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO forms (company, invoice, job) VALUES (?, ?, ?)', (company, invoice, job))
        conn.commit()
        conn.close()

        return "Form submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)

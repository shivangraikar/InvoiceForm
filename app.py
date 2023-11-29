from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'forms.db'

# Function to get a database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

# Function to close the database connection
def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Flask route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Flask route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        company = request.form['company']
        invoice = request.form['invoice']
        job = request.form['job']

        # Store data in the database
        db = get_db()
        db.execute('INSERT INTO forms (company, invoice, job) VALUES (?, ?, ?)', (company, invoice, job))
        db.commit()

        return "Form submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, g, Response, redirect, url_for
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

# Function to initialize the database
# Function to initialize the database
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        # Check if the 'forms' table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='forms'")
        table_exists = cursor.fetchone()

        if not table_exists:
            # If the 'forms' table doesn't exist, execute the schema script
            with app.open_resource('schema.sql', mode='r') as f:
                cursor.executescript(f.read())

            db.commit()


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

# Flask route for invoices
@app.route('/invoices')
def invoices():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM forms')
    entries = cursor.fetchall()
    print(entries)
    return render_template('invoices.html', entries=entries)

@app.route('/download_csv')
def download_csv():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM forms')
    entries = cursor.fetchall()

    # Create CSV content
    csv_content = "Company,Invoice,Job\n"
    for entry in entries:
        csv_content += f"{entry['company']},{entry['invoice']},{entry['job']}\n"

    # Return CSV as a response
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=forms.csv"}
    )

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Handle form submission for editing
        new_company = request.form['new_company']
        new_invoice = request.form['new_invoice']
        new_job = request.form['new_job']


        # Update the database entry with the new values
        cursor.execute('UPDATE forms SET company = ?, invoice = ?, job = ? WHERE id = ?',
               (new_company, new_invoice, new_job, entry_id))
        db.commit()

        # Redirect back to the Invoices page
        return redirect(url_for('invoices'))


    else:
        # Display the edit form pre-populated with the entry's current values
        cursor.execute('SELECT * FROM forms WHERE id = ?', (entry_id,))
        entry = cursor.fetchone()
        return render_template('edit.html', entry=entry)


# Navigation bar links
nav_links = [{'url': 'index', 'text': 'Home'}, {'url': 'invoices', 'text': 'Invoices'}]

# Flask context processors to make navigation links available to all templates
@app.context_processor
def inject_nav_links():
    return dict(nav_links=nav_links)

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)

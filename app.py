import zipfile
from flask import Flask, render_template, request, g, Response, redirect, url_for, send_file
import os, sqlite3
import uuid
from io import BytesIO
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['DATABASE'] = 'forms.db'
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder where uploaded files will be stored
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

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
def init_db():
    with app.app_context():
        db = get_db()
        try:
            with app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
            print("Database initialized successfully.")
        except Exception as e:
            print(f"Error initializing database: {e}")


# Flask route for the home page
@app.route('/')
def index():
    company_names = [
        "21st Century Concrete-Perkins",
        "50 Stars - Asbestos",
        "A.R. Baldwin Crane & Hoisting Services",
        "A9 Green/Total Green Energy Solution LLC",
        "Accurate Glass",
        "AFA Protective Systems, Inc.",
        "AJM Group Inc.",
        "American Stone Design",
        "Anderson Porter Design Inc.",
        "Anthony J. Perrone Masonry Contracting LLC",
        "Architectural Fireplaces",
        "Arlington Coal and Lumber Co. (Burlington Lumber)",
        "Bammco Construction",
        "Beacon Building Products",
        "Bernkopf Goodman LLP",
        "Boston Water and Sewer Commission",
        "BPR Companies LLC",
        "Breakaway Courier, Inc.",
        "Burgess Pest Management",
        "Burlington Lumber",
        "Cabinet Solutions",
        "Cambridge Police Detail Fund",
        "Cavicchio Greenhouses",
        "Central Steel Supply",
        "Cesar's Concrete Pumping Inc",
        "City Locksmith",
        "City of Boston",
        "City of Cambridge",
        "City of Newton",
        "Classic Stoneworks",
        "CleanBasins, Inc.",
        "CN Building Movers",
        "Columbia Design Group LLC",
        "Constitution Contracting",
        "Cornerstone Landscape Supplies Inc.",
        "Dartmouth Building Supply",
        "Dellorco & Associates",
        "Delmar Tree Landscaping Inc",
        "DFI Interiors",
        "Dileo Gas Inc.",
        "Divine Design Center",
        "Dnd Homes Procurement",
        "Drago & Toscano LLP",
        "DS Concrete Pumping Inc",
        "Eastern Environmental Inc",
        "EBI Consulting",
        "Effective Waterproofing Inc.",
        "Empire Plastering",
        "Eversource",
        "Favorite Green Energy",
        "Ferguson Enterprises LLC",
        "First Class Marble and Granite, Inc.",
        "Flush Services LLC",
        "Forest Structural Engineering",
        "Frederick W. Russell, PE",
        "Friend Building Center",
        "GeoHydroCycle, Inc.",
        "Golden Gutters",
        "Green Air Solutions, LLC",
        "Groundscapes Express, Inc.",
        "Hancock Lumber",
        "Hancock Survey Associates, Inc.",
        "Horizon Forest Products",
        "HVAC Industries Inc.",
        "Ideal Fence Inc.",
        "Independent Concrete Pumping Corp.",
        "Interstate Refrigerant Recovery, Inc",
        "J Melone & Sons, Inc.",
        "J.G. MacLellan Concrete Co. Inc.",
        "J.S. Donahue Landscaping",
        "James R. Keenan Land Surveying",
        "Jensen Hughes Inc.",
        "Jonathan Collins",
        "JP Cleaning Services",
        "K. J. Miller Mechanical, Inc.",
        "Kelly Boucher Architecture",
        "KMM Geotechnical Consultants",
        "KONE Inc.",
        "Koopman Lumber Co, Inc.",
        "Kudos Painting Inc.",
        "LaGrasse Yanowitz & Feyl Architects",
        "Landmark Door LLC",
        "Larchmont Engineering & Irrigation",
        "LEC Environmental Consultants, Inc.",
        "Linda J Brehn",
        "Localiq New England",
        "Lopez Asphalt Co.",
        "LS Fitzgerald Corp",
        "Martins Landscaping",
        "McKay Architects",
        "Metro USA Fire, Inc.",
        "MetroWest Engineering Inc",
        "MGE Construction Corp",
        "Mobile Fencing, Inc.",
        "Monte French Design Studio",
        "MV Construction & Management LLC",
        "National Grid",
        "Noble Work Carpentry Corp",
        "NPC Reprographics Company",
        "NW Pest Control Inc.",
        "O'Malley's Overhead Door Co., Inc.",
        "Oluna Cleaning Services",
        "Patriot Engineering, LLC",
        "Peter Nolan & Associates",
        "Petersen Services Inc",
        "Porcelanosa",
        "Pro-Tech America",
        "Quality Insulation & Building Products Inc.",
        "R&D Spray Technologies",
        "R.J. O'Connell & Associates, Inc.",
        "Rahall's Landscaping",
        "Ramos Finish Carpentry",
        "Raymond F. Bouley Landscaping",
        "RDK Architects",
        "Reading Asphalt Corporation",
        "Real Plan Flooring, Inc.",
        "Reskon Group Co.",
        "Richard's Iron Works",
        "Rick Cooper Paving",
        "Riemer & Braunstein LLP",
        "RLAW, P.C.",
        "RM Carpentry & Construction Inc",
        "RS Framing Experts Inc",
        "Sage Environmental, Inc.",
        "Sarno Glass & Mirror Inc",
        "Select Concrete Pumping Inc",
        "ServiceMaster by Disaster Assocaites, Inc.",
        "SERVPRO OF Allston",
        "Sobrinho Construction Inc.",
        "Sonny's Glass Tinting LLC",
        "Soriano Environmental",
        "Sox Construction Inc.",
        "Splash - The Portland Group",
        "Spolidoro and Sons Inc.",
        "Spruhan Engineering, PC",
        "TBR Excavating Inc.",
        "Ted Riley & Co d/b/a Enviro-Safe Engineering",
        "The Tile Shop LLC",
        "TJ Cashman Plumbing & Heating",
        "TJ Woods Insurance (World)",
        "TJ Woods Insurance Agency",
        "TN Carpentry",
        "Town of Brookline",
        "Town of Chelmsford",
        "Town of Lexington",
        "TR Cabinets Group",
        "Tresca Brothers Concrete, Sand & Gravel",
        "US Assure",
        "Uticon, Inc.",
        "Verdant Landscape Architecture",
        "W. Galicia Landscaping",
        "Wagon Wheel Inc.",
        "Wesley Silva Corp",
        "Wilmington Builders Supply Co. (Burlington Lumber)",
        "WIN Waste Innovations",
        "Wood & Wire Fence Co."
    ]

    job_names = [
        "100 Old River Road",
    "10-12-14 Shailer St",
    "11 Castle Rd",
    "110-112 Hampshire Street",
    "110-112 Litchfield St",
    "1256 Commonwealth Ave",
    "131 Dane Hill Rd",
    "131-133 Fayerweather St",
    "140 Wachusett Street",
    "15 Tyler Rd",
    "151-153 Babcock Street",
    "155 Middlesex Tpke",
    "16 Winchester Drive",
    "161-163 Thorndike St",
    "173 Cambridge St",
    "18 Blueberry Ln",
    "231-235 Third St",
    "23-25 Jackson St",
    "24 Blueberry Ln",
    "24 Newtonville Ave",
    "2-4 Soden Street",
    "25 Normandy Rd",
    "25-29-37 Dighton Street",
    "31 Fairlawn Ln",
    "32 Newtonville Ave",
    "356-358 Western Ave",
    "4 Revere Street",
    "40 Kent St (40 Webster)",
    "40 Oakmont Road",
    "40 Winchester Dr",
    "408-410 Western Ave",
    "43 Laconia St",
    "466 Putnam Avenue",
    "490-492 Putnam Avenue",
    "55 Green St",
    "56 Thorndike St",
    "560-562 Washington St",
    "68 Freemont St",
    "7 Spring St",
    "8 Blueberry Ln",
    "8 Poplar Rd",
    "8 Winston Road",
    "8 Winter St",
    "85 Pleasant St",
    "93 Brick Kiln Rd"
    ]
    return render_template('index.html', company_names=company_names, job_names=job_names)

# Flask route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        company = request.form['company']
        invoice = request.form['invoice']
        job = request.form['job']

        # Check if the 'pdfFile' key is in the request.files MultiDict
        print(request.files)
        if 'pdfFile' in request.files:
            pdf_file = request.files['pdfFile']

            # Generate a unique filename for the PDF using UUID
            filename = str(uuid.uuid4()) + secure_filename(pdf_file.filename)

            # Save the PDF file to a folder (create the folder if it doesn't exist)
            upload_folder = 'uploads'
            os.makedirs(upload_folder, exist_ok=True)
            pdf_file.save(os.path.join(upload_folder, filename))

            try:
                # Save the entry to the database along with the new filename
                with sqlite3.connect(app.config['DATABASE']) as conn:
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO forms (company, invoice, job, pdf_file) VALUES (?, ?, ?, ?)',
                                   (company, invoice, job, filename))
                    conn.commit()
                    print("Form submitted successfully!")

            except Exception as e:
                print(f"Error submitting form: {e}")
            
            return "Form submitted successfully!"

        else:
            print('No file uploaded.')

    return "Invalid request method."


# Route to download the uploaded PDF file
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


# Flask route for invoices
@app.route('/invoices')
def invoices():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM forms')
    entries = cursor.fetchall()
    print(entries)
    return render_template('invoices.html', entries=entries)


# Route for downloading all PDFs
@app.route('/download_all_pdfs')
def download_all_pdfs():
    db = get_db()
    cur = db.execute('SELECT id, pdf_file FROM forms')
    pdfs = cur.fetchall()

    zip_data = BytesIO()
    with zipfile.ZipFile(zip_data, 'w') as zip_file:
        for pdf in pdfs:
            pdf_data = BytesIO(pdf['pdf_file'].encode())  # Convert string to BytesIO
            zip_file.writestr(f'invoice_{pdf["id"]}.pdf', pdf_data.read())

    zip_data.seek(0)
    return send_file(zip_data, as_attachment=True, attachment_filename='all_invoices.zip')


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

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('DELETE FROM forms WHERE id = ?', (entry_id,))
    db.commit()

    return redirect(url_for('invoices'))


# Navigation bar links
nav_links = [{'url': 'index', 'text': 'Home'}, {'url': 'invoices', 'text': 'Invoices'}]

# Flask context processors to make navigation links available to all templates
@app.context_processor
def inject_nav_links():
    return dict(nav_links=nav_links)

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)

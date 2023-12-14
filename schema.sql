-- schema.sql
CREATE TABLE IF NOT EXISTS forms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    invoice TEXT NOT NULL,
    job TEXT NOT NULL,
    pdf_file BLOB NOT NULL
);

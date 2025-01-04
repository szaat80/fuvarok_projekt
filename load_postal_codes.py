import pandas as pd
import sqlite3

def load_postal_codes_from_xls(file_path: str, db_path: str):
    # Beolvasás az .xls fájlból
    df = pd.read_excel(file_path)

    # Kapcsolódás az SQLite adatbázishoz
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Táblázat létrehozása, ha nem létezik
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS postal_codes (
            postal_code TEXT PRIMARY KEY,
            city TEXT NOT NULL,
            county TEXT
        )
    ''')

    # Adatok betöltése az adatbázisba
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT OR IGNORE INTO postal_codes (postal_code, city, county)
            VALUES (?, ?, ?)
        ''', (row['Irányítószám'], row['Település'], row['Megye']))

    # Változások mentése és kapcsolat lezárása
    conn.commit()
    conn.close()

# Használat példa
load_postal_codes_from_xls('postal_codes.xls', 'postal_codes.db')







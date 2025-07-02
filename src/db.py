import sqlite3
from .utils import hash_password # Importiert hash_password aus demselben Paket (src)

# Pfad zur Datenbankdatei relativ zum Hauptskript (datenbank.py)
DB_NAME = "users.db"

def init_db():
    """Initializes the database, creates the users table, and adds the admin user if not exists."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        # Create table if it doesn't exist
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        conn.commit() # Commit table creation

        # Soldaten-Tabelle anlegen (Personalnummer als Primärschlüssel)
        c.execute('''
            CREATE TABLE IF NOT EXISTS soldiers (
                personalnummer TEXT PRIMARY KEY,
                dienstgrad TEXT NOT NULL,
                name TEXT NOT NULL,
                vorname TEXT NOT NULL,
                personenkennziffer TEXT,
                geburtsdatum TEXT,
                geburtsort TEXT,
                telefonnummer TEXT,
                marine INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

        # Attempt to create the admin user (only if it doesn't exist)
        try:
            c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                     ("admin", hash_password("admin123")))
            conn.commit() # Commit admin user creation
            print("Admin user created.") # Optional: Ausgabe zur Info beim ersten Start
        except sqlite3.IntegrityError:
            # Admin user already exists, ignore.
            print("Admin user already exists.") # Optional
            pass

    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        if conn:
            conn.close()

def authenticate_user(username, password):
    """Authenticates a user against the database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        result = c.fetchone()

        # Vergleiche den Hash des eingegebenen Passworts mit dem gespeicherten Hash
        if result and result[0] == hash_password(password):
            return True # Authentifizierung erfolgreich
        else:
            return False # Authentifizierung fehlgeschlagen

    except Exception as e:
        print(f"Database authentication error: {e}")
        return False # Rückgabe False im Fehlerfall
    finally:
        if conn:
            conn.close()

def get_settings():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.commit()
    c.execute("SELECT key, value FROM settings")
    result = dict(c.fetchall())
    conn.close()
    return result

def save_settings(settings: dict):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    for key, value in settings.items():
        c.execute("REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def insert_soldier(soldier: dict):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO soldiers (
            personalnummer, dienstgrad, name, vorname, personenkennziffer, geburtsdatum, geburtsort, telefonnummer, marine
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        soldier["personalnummer"],
        soldier["dienstgrad"],
        soldier["name"],
        soldier["vorname"],
        soldier.get("personenkennziffer", None),
        soldier.get("geburtsdatum", None),
        soldier.get("geburtsort", None),
        soldier.get("telefonnummer", None),
        1 if soldier.get("marine") else 0
    ))
    conn.commit()
    conn.close()

def get_all_soldiers():
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT personalnummer, dienstgrad, name, vorname, personenkennziffer, geburtsdatum, geburtsort, telefonnummer, marine FROM soldiers")
        rows = c.fetchall()
        return [
            {
                "personalnummer": row[0],
                "dienstgrad": row[1],
                "name": row[2],
                "vorname": row[3],
                "personenkennziffer": row[4],
                "geburtsdatum": row[5],
                "geburtsort": row[6],
                "telefonnummer": row[7],
                "marine": bool(row[8])
            }
            for row in rows
        ]
    except sqlite3.Error as e:
        print(f"Datenbankfehler beim Laden der Soldaten: {e}")
        return []
    finally:
        if conn:
            conn.close()

def delete_soldier(personalnummer):
    """
    Löscht einen Soldaten aus der Datenbank.

    Args:
        personalnummer (str): Die Personalnummer des zu löschenden Soldaten

    Returns:
        bool: True wenn erfolgreich gelöscht, False wenn ein Fehler aufgetreten ist
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('DELETE FROM soldiers WHERE personalnummer = ?', (personalnummer,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Datenbankfehler beim Löschen des Soldaten: {e}")
        return False
    finally:
        if conn:
            conn.close()

def update_soldier(personalnummer, updated_fields: dict):
    """
    Aktualisiert die Daten eines Soldaten anhand der Personalnummer.

    Args:
        personalnummer (str): Die Personalnummer des zu aktualisierenden Soldaten
        updated_fields (dict): Die zu aktualisierenden Felder und deren neue Werte

    Returns:
        bool: True wenn erfolgreich aktualisiert, False wenn ein Fehler aufgetreten ist
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        # Dynamisch das SQL-Statement bauen
        set_clause = ", ".join([f"{key}=?" for key in updated_fields.keys()])
        values = list(updated_fields.values())
        values.append(personalnummer)
        sql = f"UPDATE soldiers SET {set_clause} WHERE personalnummer = ?"
        c.execute(sql, values)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Datenbankfehler beim Aktualisieren des Soldaten: {e}")
        return False
    finally:
        if conn:
            conn.close()

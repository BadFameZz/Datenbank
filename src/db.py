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

import flet as ft
# Importiert notwendige Funktionen und Klassen aus dem 'src'-Paket
# Stellen Sie sicher, dass der 'src'-Ordner und die darin enthaltenen Dateien
# (db.py, utils.py, views/login_view.py, views/dashboard_view.py) existieren
# und die korrekten Inhalte haben, wie zuvor besprochen.
from src.db import init_db
from src.views.login_view import LoginView
from src.views.dashboard_view import create_dashboard_view

def main(page: ft.Page):
    """
    The main function that sets up the Flet page and handles view switching.
    """
    # Flet Page Grundeinstellungen
    page.title = "Datenbank Anwendung" # Ein passenderer Titel für die Hauptapp
    page.theme_mode = ft.ThemeMode.DARK
    page.window.full_screen = True
    page.window.visible = True
    page.padding = 0

    # --- Logik zum Umschalten zwischen den Ansichten ---
    def show_login_view():
        """Clears the page and displays the LoginView."""
        page.clean() # Entfernt alle aktuellen Steuerelemente von der Seite
        # Erstellt eine Instanz der LoginView-Klasse
        # Übergibt die aktuelle Seite und die Funktion zum Anzeigen des Dashboards bei Erfolg
        login_view_control = LoginView(page=page, on_login_success=show_dashboard_view)
        page.add(login_view_control) # Fügt die LoginView zur Seite hinzu
        page.update() # Aktualisiert die Seite, um die Änderungen anzuzeigen

    def show_dashboard_view():
        """Clears the page and displays the Dashboard view."""
        page.clean() # Entfernt alle aktuellen Steuerelemente von der Seite
        # Erstellt die Dashboard-Ansicht
        dashboard_view_control = create_dashboard_view(page=page)
        page.add(dashboard_view_control) # Fügt die Dashboard-Ansicht zur Seite hinzu
        page.update() # Aktualisiert die Seite, um die Änderungen anzuzeigen
    # --- Ende Logik zum Umschalten ---

    # Starte die Anwendung, indem die anfängliche Ansicht (Login) angezeigt wird
    show_login_view()

# --- Anwendungsstart ---
# Zuerst die Datenbank initialisieren (Tabelle und Admin-Benutzer erstellen/prüfen)
# Dies geschieht, bevor die Flet GUI-Anwendung gestartet wird.
# Stellen Sie sicher, dass die init_db Funktion in src/db.py korrekt implementiert ist.
print("Initialisiere Datenbank...") # Optional: Konsolenausgabe zur Information
init_db()
print("Datenbank initialisierung abgeschlossen.") # Optional

# Startet die Flet GUI-Anwendung, die die 'main' Funktion aufruft
ft.app(target=main)

# Diese Datei (datenbank.py) ist nun der zentrale Einstiegspunkt.
# Sie importiert und nutzt die verschiedenen Module aus dem 'src'-Ordner,
# um die Datenbank zu initialisieren und die Benutzeroberfläche zu verwalten.

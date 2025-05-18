import flet as ft
# Importiert authenticate_user und hash_password aus den Modulen in 'src'
# Die '..' bedeuten "gehe ein Verzeichnis hoch" (von views zu src)
from ..db import authenticate_user
from ..utils import hash_password

# Verwenden einer Klasse für die Login-Ansicht zur besseren Verwaltung der UI-Elemente
class LoginView(ft.Container):
    def __init__(self, page: ft.Page, on_login_success):
        # Initialisiert den ft.Container als Basis für die Ansicht
        super().__init__(
            alignment=ft.alignment.center,
            expand=True,
        )
        self.page = page
        self.on_login_success = on_login_success # Callback-Funktion, die bei Erfolg aufgerufen wird

        # Definieren der UI-Elemente als Instanzvariablen
        self.username = ft.TextField(label="Benutzername", prefix_icon=ft.Icons.PERSON, width=300)
        self.password = ft.TextField(label="Passwort", prefix_icon=ft.Icons.LOCK, password=True, can_reveal_password=True, width=300)
        self.loading = ft.ProgressRing(visible=False)
        self.error_text = ft.Text("", color=ft.Colors.RED_400)
        # login_btn ruft die handle_login Methode dieser Klasse auf
        self.login_btn = ft.ElevatedButton(text="Login", width=300, on_click=self.handle_login)

        # Definieren des Inhalts (Layouts) des Containers
        self.content = ft.Column(
            [
                ft.Text("Login", size=32, weight=ft.FontWeight.BOLD),
                self.username,
                self.password,
                self.error_text,
                ft.Row([self.login_btn, self.loading], alignment="center", spacing=10),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

    def handle_login(self, e):
        """Handles the login button click event."""
        u = self.username.value.strip()
        p = self.password.value.strip()

        if not u or not p:
            self.error_text.value = "Benutzername und Passwort erforderlich"
            self.page.update()
            return

        self.loading.visible = True
        self.error_text.value = ""
        self.login_btn.disabled = True
        self.page.update()

        # Authentifizierung über die Funktion im db-Modul
        if authenticate_user(u, p):
            # Login erfolgreich - rufe die übergebene Callback-Funktion auf
            self.on_login_success()
        else:
            # Login fehlgeschlagen
            self.error_text.value = "Falscher Benutzername oder Passwort"
            # UI-Elemente für neuen Versuch zurücksetzen
            self.loading.visible = False
            self.login_btn.disabled = False
            self.page.update()

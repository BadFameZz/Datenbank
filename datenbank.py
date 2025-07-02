import flet as ft
from src.theme import get_theme
from src.db import init_db
from src.views.login_view import LoginView
from src.views.dashboard_view import create_dashboard_view

def main(page: ft.Page):
    """
    The main function that sets up the Flet page and handles view switching.
    """
    # Flet Page Grundeinstellungen
    page.title = "Datenbank Anwendung"
    page.theme_mode = ft.ThemeMode.DARK
    # Start im Vollbild und automatisch an die Bildschirmauflösung anpassen
    page.window.full_screen = True
    page.window.visible = True
    page.padding = 0
    page.on_resize = lambda e: page.update()

    def get_mode():
        return "dark" if page.theme_mode == ft.ThemeMode.DARK else "light"

    # Setze Theme und Hintergrundfarbe zentral
    theme = get_theme(get_mode())
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE_ACCENT_700,
    )
    page.bgcolor = theme["bg"]

    def show_login_view():
        page.clean()
        theme = get_theme(get_mode())
        page.bgcolor = theme["bg"]
        page.update()
        login_view_control = LoginView(page=page, on_login_success=show_dashboard_view)
        page.add(login_view_control)
        page.update()

    def show_dashboard_view():
        page.clean()
        theme = get_theme(get_mode())
        page.bgcolor = theme["bg"]
        page.update()
        dashboard_view_control = create_dashboard_view(page=page)
        page.add(dashboard_view_control)
        page.update()

    show_login_view()

print("Initialisiere Datenbank...")
init_db()
print("Datenbank initialisierung abgeschlossen.")
ft.app(target=main, view=ft.AppView.FLET_APP)

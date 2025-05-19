import flet as ft
from src.theme import get_theme

def create_settings_view(page: ft.Page):
    theme = get_theme("dark" if page.theme_mode == ft.ThemeMode.DARK else "light")
    logo_path = page.session.get("sidebar_logo") or "/Users/badfamezz/code/datenbank/assets/logos/wappen.png"
    sidebar_title = page.session.get("sidebar_title") or "Datenbank"

    logo_field = ft.TextField(
        label="Pfad zum neuen Wappen (Logo)",
        value=logo_path,
        width=300
    )
    title_field = ft.TextField(
        label="Sidebar-Titel",
        value=sidebar_title,
        width=300
    )

    def save_settings(e):
        page.session.set("sidebar_logo", logo_field.value)
        page.session.set("sidebar_title", title_field.value)
        from src.views.dashboard_view import create_dashboard_view
        page.clean()
        page.add(create_dashboard_view(page))

    def cancel(e):
        from src.views.dashboard_view import create_dashboard_view
        page.clean()
        page.add(create_dashboard_view(page))

    return ft.Container(
        alignment=ft.alignment.center,
        expand=True,
        content=ft.Column([
            ft.Text("Einstellungen", size=28, weight=ft.FontWeight.BOLD, color=theme["text"]),
            logo_field,
            title_field,
            ft.Row([
                ft.ElevatedButton("Speichern", on_click=save_settings, bgcolor=theme["button"], color=theme["button_text"]),
                ft.TextButton("Abbrechen", on_click=cancel)
            ], alignment=ft.MainAxisAlignment.END, spacing=10)
        ], spacing=20, width=400, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

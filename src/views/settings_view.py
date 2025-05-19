import flet as ft
from src.theme import get_theme
from src.views.sidebar import Sidebar
import sqlite3
from src.db import get_settings, save_settings

def create_settings_view(page: ft.Page):
    theme = get_theme("dark" if page.theme_mode == ft.ThemeMode.DARK else "light")

    # Werte aus Datenbank laden
    settings = get_settings()
    logo_path = settings.get("sidebar_logo") or "/Users/badfamezz/code/datenbank/assets/logos/wappen.png"
    sidebar_title = settings.get("sidebar_title") or "Datenbank"

    logo_field = ft.TextField(
        label="Pfad zum neuen Wappen (Logo)",
        value=logo_path,
        width=600
    )
    title_field = ft.TextField(
        label="Sidebar-Titel",
        value=sidebar_title,
        width=600
    )

    def save_settings_action(e):
        save_settings({
            "sidebar_logo": logo_field.value,
            "sidebar_title": title_field.value
        })
        from src.views.dashboard_view import create_dashboard_view
        page.clean()
        page.add(create_dashboard_view(page))

    def cancel(e):
        from src.views.dashboard_view import create_dashboard_view
        page.clean()
        page.add(create_dashboard_view(page))

    # Header wie im Dashboard, aber ohne Logout-Button
    menu_btn = ft.IconButton(
        icon=ft.Icons.MENU,
        icon_color="#ffffff",
        on_click=lambda e: setattr(page, 'sidebar_collapsed', not getattr(page, 'sidebar_collapsed', False)) or page.clean() or page.add(create_settings_view(page)),
    )
    header = ft.Container(
        height=60,
        bgcolor=theme["header"],
        padding=ft.padding.symmetric(horizontal=20),
        content=ft.Row([
            menu_btn,
            ft.Text("Einstellungen", size=24, weight=ft.FontWeight.BOLD, color="#ffffff", expand=True),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

    sidebar = Sidebar(page, theme, lambda e: page.theme_mode == ft.ThemeMode.LIGHT, getattr(page, 'sidebar_collapsed', False)).get()

    # Modernes, grid-basiertes Card-Design für Settings
    branding_card = ft.Container(
        bgcolor=theme["sidebar"],
        border_radius=ft.border_radius.all(16),
        padding=ft.padding.all(32),
        margin=ft.margin.only(bottom=24),
        shadow=ft.BoxShadow(
            color="#00000022",
            blur_radius=16,
            offset=ft.Offset(0, 4)
        ),
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.BRUSH, color=theme["button"], size=28),
                ft.Text("Branding", size=20, weight=ft.FontWeight.BOLD, color=theme["text"]),
            ], spacing=12, alignment=ft.MainAxisAlignment.START),
            ft.Divider(height=16, color=theme["sidebar_divider"]),
            ft.Container(
                content=ft.Image(
                    src=logo_path,
                    width=60,
                    height=60,
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=10),
            ),
            title_field,
            logo_field,
        ], spacing=18, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    # Beispiel für weitere Sektionen (Platzhalter)
    placeholder_card = lambda title: ft.Container(
        bgcolor=theme["sidebar"],
        border_radius=ft.border_radius.all(16),
        padding=ft.padding.all(32),
        margin=ft.margin.only(bottom=24),
        shadow=ft.BoxShadow(
            color="#00000022",
            blur_radius=16,
            offset=ft.Offset(0, 4)
        ),
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.SETTINGS, color=theme["button"], size=28),
                ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=theme["text"]),
            ], spacing=12, alignment=ft.MainAxisAlignment.START),
            ft.Divider(height=16, color=theme["sidebar_divider"]),
            ft.Text("Hier kann weiteres Setting hin.", color=theme["text_secondary"])
        ], spacing=18, horizontal_alignment=ft.CrossAxisAlignment.START)
    )

    actions = ft.Row([
        ft.ElevatedButton("Speichern", on_click=save_settings_action, bgcolor=theme["button"], color=theme["button_text"]),
        ft.TextButton("Abbrechen", on_click=cancel)
    ], alignment=ft.MainAxisAlignment.END, spacing=10)

    # Grid-Layout für die Cards
    grid = ft.GridView(
        controls=[
            branding_card,
            placeholder_card("Benutzerverwaltung"),
            placeholder_card("Sicherheit"),
        ],
        expand=True,
        runs_count=2,
        max_extent=600,
        child_aspect_ratio=1.2,
        spacing=24,
        run_spacing=24,
        padding=ft.padding.symmetric(horizontal=32),
    )

    content = ft.Container(
        alignment=ft.alignment.top_center,
        expand=True,
        content=ft.Column([
            grid,
            actions
        ], spacing=32, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    layout = ft.Row([
        sidebar,
        ft.Column([
            header,
            content,
        ], expand=True)
    ], spacing=0, expand=True)

    return layout

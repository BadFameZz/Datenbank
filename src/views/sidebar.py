import flet as ft
from src.theme import get_theme
from src.db import get_settings

class Sidebar:
    def __init__(self, page, theme, on_toggle, collapsed):
        self.page = page
        self.theme = theme
        self.on_toggle = on_toggle
        self.collapsed = collapsed
        self.build_sidebar()

    def open_settings_view(self, e):
        from src.views.settings_view import create_settings_view
        self.page.clean()
        self.page.add(create_settings_view(self.page))

    def build_sidebar(self):
        # Branding-Werte immer frisch aus der Datenbank laden
        settings = get_settings()
        logo_path = settings.get("sidebar_logo") or "/Users/badfamezz/code/datenbank/assets/logos/wappen.png"
        sidebar_title = settings.get("sidebar_title") or "Datenbank"
        logo = ft.Container(
            content=ft.Image(
                src=logo_path,
                width=60,
                height=60,
            ),
            alignment=ft.alignment.top_center,
            padding=ft.padding.only(bottom=10, top=0),
        )
        title = ft.Container(
            content=ft.Text(
                sidebar_title,
                size=20,
                weight=ft.FontWeight.BOLD,
                color=self.theme["text"],
                text_align=ft.TextAlign.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(bottom=5),
        )
        self.menu_column = ft.Column(
            [
                logo,
                title,
                ft.Divider(color=self.theme["sidebar_divider"]),
                ft.TextButton(text="Übersicht", on_click=lambda e: print("Übersicht geklickt"), style=ft.ButtonStyle(color=self.theme["text_secondary"])),
                ft.TextButton(text="Soldat hinzufügen", on_click=lambda e: print("Soldat hinzufügen"), style=ft.ButtonStyle(color=self.theme["text_secondary"])),
                ft.TextButton(text="Einstellungen", on_click=self.open_settings_view, style=ft.ButtonStyle(color=self.theme["text_secondary"])),
                ft.Divider(color=self.theme["sidebar_divider"]),
                ft.Row(
                    [
                        ft.Text("Dark", color=self.theme["text_secondary"]),
                        ft.Switch(value=self.page.theme_mode == ft.ThemeMode.DARK, on_change=self.on_toggle),
                        ft.Text("Light", color=self.theme["text_secondary"]),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5
                )
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        )
        # Im eingeklappten Zustand nur das Logo anzeigen, aber oben ausrichten
        self.content = ft.Container(
            width=200 if not self.collapsed else 60,
            bgcolor=self.theme["sidebar"],
            padding=ft.padding.all(10),
            content=self.menu_column if not self.collapsed else ft.Column([
                logo
            ], alignment=ft.MainAxisAlignment.START),
        )

    def get(self):
        return self.content

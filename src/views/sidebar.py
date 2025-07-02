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
        self.page.update()

    def open_data_view(self, e):
        from src.views.data_view import create_data_view
        self.page.clean()
        layout = create_data_view(self.page)
        if layout:
            self.page.add(layout)
            self.page.update()

    def open_dashboard_view(self, e):
        from src.views.dashboard_view import create_dashboard_view
        self.page.clean()
        self.page.add(create_dashboard_view(self.page))
        self.page.update()

    def open_add_soldier_view(self, e):
        from src.views.add_soldier_view import create_add_soldier_view
        self.page.clean()
        self.page.add(create_add_soldier_view(self.page))
        self.page.update()

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
                ft.TextButton(text="Übersicht", on_click=self.open_dashboard_view, style=ft.ButtonStyle(color=self.theme["text_secondary"])),
                ft.TextButton(text="Daten", on_click=self.open_data_view, style=ft.ButtonStyle(color=self.theme["text_secondary"])),
                ft.TextButton(text="Soldat hinzufügen", on_click=self.open_add_soldier_view, style=ft.ButtonStyle(color=self.theme["text_secondary"])),
                ft.TextButton(text="Einstellungen", on_click=self.open_settings_view, style=ft.ButtonStyle(color=self.theme["text_secondary"])),
                ft.Divider(color=self.theme["sidebar_divider"]),
                ft.Row(
                    [
                        ft.Text("Dark", color=self.theme["text_secondary"]),
                        ft.Switch(value=self.page.theme_mode == ft.ThemeMode.DARK, on_change=self._toggle_theme),
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
            padding=ft.padding.only(top=20),  # Ursprüngliches Padding wiederhergestellt
            content=self.menu_column if not self.collapsed else ft.Column([
                logo
            ], alignment=ft.MainAxisAlignment.START),
        )

    def get(self):
        return self.content

    def _toggle_theme(self, e):
        self.page.theme_mode = ft.ThemeMode.LIGHT if self.page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        self.page.update()
        # Seite neu laden, damit das Theme überall übernommen wird
        if hasattr(self.page, 'current_view') and callable(self.page.current_view):
            self.page.clean()
            self.page.add(self.page.current_view(self.page))
        else:
            self.page.clean()
            from src.views.dashboard_view import create_dashboard_view
            self.page.add(create_dashboard_view(self.page))

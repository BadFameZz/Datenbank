import flet as ft
from src.theme import get_theme

class Sidebar:
    def __init__(self, page, theme, on_toggle, collapsed):
        self.page = page
        self.theme = theme
        self.on_toggle = on_toggle
        self.collapsed = collapsed
        self.build_sidebar()

    def open_settings(self, e):
        def save_settings(ev):
            # Werte speichern (hier nur als Beispiel, persistente Speicherung kann ergänzt werden)
            self.page.session.set("sidebar_logo", logo_field.value)
            self.page.session.set("sidebar_title", title_field.value)
            self.page.clean()
            self.page.add(self.page.current_view())

        logo_field = ft.TextField(
            label="Pfad zum neuen Wappen (Logo)",
            value=self.page.session.get("sidebar_logo") or "/Users/badfamezz/code/datenbank/assets/logos/wappen.png",
            width=300
        )
        title_field = ft.TextField(
            label="Sidebar-Titel",
            value=self.page.session.get("sidebar_title") or "Datenbank",
            width=300
        )
        dialog = ft.AlertDialog(
            title=ft.Text("Einstellungen Sidebar"),
            content=ft.Column([
                logo_field,
                title_field
            ], spacing=10),
            actions=[
                ft.TextButton("Speichern", on_click=save_settings),
                ft.TextButton("Abbrechen", on_click=lambda ev: self.page.dialog.close())
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def open_settings_view(self, e):
        from src.views.settings_view import create_settings_view
        self.page.clean()
        self.page.add(create_settings_view(self.page))

    def build_sidebar(self):
        logo_path = self.page.session.get("sidebar_logo") or "/Users/badfamezz/code/datenbank/assets/logos/wappen.png"
        sidebar_title = self.page.session.get("sidebar_title") or "Datenbank"
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

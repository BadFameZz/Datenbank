import flet as ft
from src.theme import get_theme
from src.views.sidebar import Sidebar

def create_data_view(page: ft.Page):
    theme = get_theme("dark" if page.theme_mode == ft.ThemeMode.DARK else "light")
    sidebar = Sidebar(page, theme, lambda e: page.theme_mode == ft.ThemeMode.LIGHT, getattr(page, 'sidebar_collapsed', False)).get()

    header = ft.Container(
        height=60,
        bgcolor=theme["header"],
        padding=ft.padding.symmetric(horizontal=20),
        content=ft.Row([
            ft.IconButton(
                icon=ft.Icons.MENU,
                icon_color="#ffffff",
                on_click=lambda e: setattr(page, 'sidebar_collapsed', not getattr(page, 'sidebar_collapsed', False)) or page.clean() or page.add(create_data_view(page)),
            ),
            ft.Text("Daten", size=24, weight=ft.FontWeight.BOLD, color="#ffffff", expand=True),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

    main_content = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Text("Hier können später Daten angezeigt werden.", color=theme["text_secondary"], size=18)
    )

    layout = ft.Row([
        sidebar,
        ft.Column([
            header,
            main_content,
        ], expand=True)
    ], spacing=0, expand=True)

    return layout

import flet as ft
from src.theme import get_theme
from src.views.sidebar import Sidebar

def create_dashboard_view(page: ft.Page):
    page.current_view = create_dashboard_view
    def get_mode():
        return "dark" if page.theme_mode == ft.ThemeMode.DARK else "light"

    # State für Sidebar collapsed
    if not hasattr(page, "sidebar_collapsed"):
        page.sidebar_collapsed = False

    def toggle_theme_mode(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        theme = get_theme(get_mode())
        page.bgcolor = theme["bg"]
        page.update()
        page.clean()
        page.add(create_dashboard_view(page))

    def toggle_sidebar(e):
        page.sidebar_collapsed = not page.sidebar_collapsed
        page.clean()
        page.add(create_dashboard_view(page))

    theme = get_theme(get_mode())
    page.bgcolor = theme["bg"]

    def logout(e):
        page.clean()
        from src.views.login_view import LoginView
        page.add(LoginView(page=page, on_login_success=lambda: page.add(create_dashboard_view(page))))
        page.update()
        

    # Menü-Button in den Header
    menu_btn = ft.IconButton(
        icon=ft.Icons.MENU,
        icon_color="#ffffff",
        on_click=toggle_sidebar,
    )

    header = ft.Container(
        height=60,
        bgcolor=theme["header"],
        padding=ft.padding.symmetric(horizontal=20),
        content=ft.Row([
            menu_btn,
            ft.Text("Dashboard", size=24, weight=ft.FontWeight.BOLD, color="#ffffff", expand=True),
            ft.ElevatedButton(
                text="Logout",
                bgcolor=theme["back_button"],
                color="#ffffff",
                on_click=logout,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=2),
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

    main_content = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Column(
            [
                ft.Text("Willkommen im Dashboard!", size=32, weight=ft.FontWeight.BOLD, color=theme["text"]),
                ft.Text("Dies ist Ihr leeres Dashboard.", size=16, color=theme["text_secondary"]),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
    )

    sidebar = Sidebar(page, theme, toggle_theme_mode, page.sidebar_collapsed).get()

    layout = ft.Row([
        sidebar,
        ft.Column([
            header,
            main_content
        ], expand=True)
    ], spacing=0, expand=True)

    return layout

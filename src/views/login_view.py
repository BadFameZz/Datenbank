import flet as ft
from ..db import authenticate_user
from ..utils import hash_password
from ..theme import get_theme

class LoginView(ft.Container):
    def __init__(self, page: ft.Page, on_login_success):
        theme = get_theme("dark" if page.theme_mode == ft.ThemeMode.DARK else "light")
        super().__init__(
            bgcolor=theme["bg"],
            alignment=ft.alignment.center,
            expand=True,
        )
        self.page = page
        self.on_login_success = on_login_success
        self.theme = theme

        self.app_logo_top = ft.Image(
            src='/Users/badfamezz/code/datenbank/assets/logos/wappen.png',
            width=100,
            height=100,
        )
        self.app_title = ft.Text(
            "Datenbank1",
            size=25,
            weight=ft.FontWeight.BOLD,
            color=theme["text"]
        )
        self.username = ft.TextField(
            label="Benutzername",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.WHITE24,
            focused_border_color=ft.Colors.BLUE_ACCENT_700,
            bgcolor=ft.Colors.WHITE10,
            border_radius=ft.border_radius.all(10),
            width=300,
            color=theme["text"],
            label_style=ft.TextStyle(color=ft.Colors.WHITE54),
            cursor_color=ft.Colors.BLUE_ACCENT_700,
            prefix_icon=ft.Icons.PERSON_OUTLINE_ROUNDED,
            content_padding=ft.padding.symmetric(vertical=15, horizontal=10),
        )
        self.password = ft.TextField(
            label="Passwort",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.WHITE24,
            focused_border_color=ft.Colors.BLUE_ACCENT_700,
            bgcolor=ft.Colors.WHITE10,
            border_radius=ft.border_radius.all(10),
            width=300,
            password=True,
            can_reveal_password=True,
            color=theme["text"],
            label_style=ft.TextStyle(color=ft.Colors.WHITE54),
            cursor_color=ft.Colors.BLUE_ACCENT_700,
            prefix_icon=ft.Icons.LOCK_OUTLINE_ROUNDED,
            content_padding=ft.padding.symmetric(vertical=15, horizontal=10),
            on_submit=self.handle_login,
        )
        self.loading = ft.ProgressRing(visible=False, width=20, height=20, stroke_width=2, color=ft.Colors.BLUE_ACCENT_700)
        self.error_text = ft.Text("", color=ft.Colors.RED_ACCENT_700, size=12)
        self.login_button = ft.ElevatedButton(
            text="Login",
            on_click=self.handle_login,
            bgcolor=theme["button"],
            color=theme["button_text"],
            width=200,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                elevation=5,
            ),
        )
        self.framed_content = ft.Container(
            width=350,
            height=500,
            bgcolor=theme["sidebar"],
            border_radius=ft.border_radius.all(10),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS_WITH_SAVE_LAYER,
            shadow=ft.BoxShadow(
                color=ft.Colors.BLACK26,
                blur_radius=10,
                offset=ft.Offset(0, 2)
            ),
            content=ft.Column(
                [
                    ft.Container(
                        bgcolor=ft.Colors.BLUE_ACCENT_700,
                        expand=1,
                        content=ft.Column([
                            self.app_logo_top,
                            self.app_title,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10
                        ),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        bgcolor=theme["sidebar"],
                        expand=2,
                        padding=ft.padding.only(top=50),
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            self.username,
                                            self.password,
                                            self.error_text,
                                        ],
                                        spacing=15,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        width=300,
                                    ),
                                    padding=ft.padding.only(top=40),
                                    alignment=ft.alignment.center,
                                ),
                                self.login_button,
                                ft.Row([self.loading], alignment=ft.MainAxisAlignment.CENTER)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20
                        ),
                        alignment=ft.alignment.top_center,
                    ),
                ],
                expand=True,
                spacing=0
            ),
            alignment=ft.alignment.center,
        )
        self.content = self.framed_content

    def handle_login(self, e):
        u = self.username.value.strip()
        p = self.password.value.strip()
        if not u or not p:
            self.error_text.value = "Benutzername und Passwort erforderlich"
            self.page.update()
            return
        self.loading.visible = True
        self.error_text.value = ""
        self.login_button.disabled = True
        self.username.disabled = True
        self.password.disabled = True
        self.page.update()
        if authenticate_user(u, p):
            self.on_login_success()
        else:
            self.error_text.value = "Falscher Benutzername oder Passwort"
            self.loading.visible = False
            self.login_button.disabled = False
            self.username.disabled = False
            self.password.disabled = False
            self.page.update()

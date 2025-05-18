import flet as ft

def create_dashboard_view(page: ft.Page):
    """Creates the Flet controls for the dashboard view."""
    return ft.Container(
        alignment=ft.alignment.center,
        expand=True,
        content=ft.Column(
            [
                ft.Text("Willkommen im Dashboard!", size=32, weight=ft.FontWeight.BOLD),
                ft.Text("Dies ist Ihr leeres Dashboard.", size=16),
                # Hier könnten Sie später weitere Dashboard-Elemente hinzufügen
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

import flet as ft
from .table_utils import build_table_rows, build_table_columns

def build_igf_table(soldiers_sorted, theme, page):
    return ft.Container(
        expand=True,
        alignment=ft.alignment.top_center,
        padding=ft.padding.all(20),
        content=ft.ListView(
            expand=True,
            spacing=0,
            padding=0,
            controls=[
                ft.Container(
                    content=ft.DataTable(
                        columns=build_table_columns(),
                        rows=build_table_rows(soldiers_sorted),
                        border=ft.border.all(0, "transparent"),
                        heading_row_color="#ededec" if page.theme_mode == "light" else theme["sidebar"],
                        heading_row_height=48,
                        data_row_color={"even": "#fff" if page.theme_mode == "light" else theme["sidebar"], "odd": "#f8f8fa" if page.theme_mode == "light" else theme["bg"]},
                        data_text_style=ft.TextStyle(color="#000" if page.theme_mode == "light" else theme["text"], size=14),
                        divider_thickness=0.5,
                        horizontal_margin=0,
                        column_spacing=10,
                        show_checkbox_column=False,
                        expand=True,
                        border_radius=ft.border_radius.all(12),
                    ),
                    padding=0,
                    expand=True
                )
            ]
        )
    )

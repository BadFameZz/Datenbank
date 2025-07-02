import flet as ft

def build_table_rows(soldiers_sorted):
    return [
        ft.DataRow(cells=[
            ft.DataCell(ft.Text(str(idx + 1), text_align=ft.TextAlign.LEFT)),
            ft.DataCell(ft.Text(s["dienstgrad"], text_align=ft.TextAlign.LEFT)),
            ft.DataCell(ft.Text(s["name"], text_align=ft.TextAlign.LEFT)),
        ]) for idx, s in enumerate(soldiers_sorted)
    ]

def build_table_columns():
    return [
        ft.DataColumn(label=ft.Text("Nr.", text_align=ft.TextAlign.LEFT), numeric=True),
        ft.DataColumn(label=ft.Text("DG", text_align=ft.TextAlign.LEFT)),
        ft.DataColumn(label=ft.Text("Name", text_align=ft.TextAlign.LEFT)),
    ]

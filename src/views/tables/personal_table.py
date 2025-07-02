import flet as ft

def make_edit_callback(soldat, open_popup):
    def callback(e):
        print(f"Bearbeiten geklickt: {soldat['personalnummer']}")
        open_popup(soldat)
    return callback

def make_delete_callback(soldat, delete_soldier):
    def callback(e):
        print(f"Löschen geklickt: {soldat['personalnummer']}")
        delete_soldier(soldat)
    return callback

def build_personal_table(soldiers_sorted, theme, page, open_popup, delete_soldier):
    table_rows = [
        ft.DataRow(cells=[
            ft.DataCell(ft.Text(str(idx + 1), text_align=ft.TextAlign.LEFT)),
            ft.DataCell(ft.Text(s["dienstgrad"], text_align=ft.TextAlign.LEFT)),
            ft.DataCell(ft.Text(s["name"], text_align=ft.TextAlign.LEFT)),
            ft.DataCell(ft.Text(s["vorname"], text_align=ft.TextAlign.LEFT)),
            ft.DataCell(ft.Text(s["personalnummer"], text_align=ft.TextAlign.LEFT)),
            ft.DataCell(ft.Text(s["personenkennziffer"] or "", text_align=ft.TextAlign.LEFT)),
            ft.DataCell(ft.Text(s["geburtsdatum"] or "", text_align=ft.TextAlign.LEFT)),
            ft.DataCell(ft.Text(s["geburtsort"] or "", text_align=ft.TextAlign.LEFT)),
            ft.DataCell(ft.Text(s["telefonnummer"] or "", text_align=ft.TextAlign.LEFT)),
            ft.DataCell(
                ft.Row(
                    [
                        ft.TextButton(
                            content=ft.Row([
                                ft.Icon(ft.Icons.EDIT, size=18),
                                ft.Text("Bearbeiten")
                            ], spacing=4),
                            tooltip="Bearbeiten",
                            on_click=make_edit_callback(s, open_popup),
                            style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=8, vertical=2)),
                        ),
                        ft.TextButton(
                            content=ft.Row([
                                ft.Icon(ft.Icons.DELETE, size=18, color=ft.Colors.RED_500),
                                ft.Text("Löschen", color=ft.Colors.RED_500)
                            ], spacing=4),
                            tooltip="Löschen",
                            on_click=make_delete_callback(s, delete_soldier),
                            style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=8, vertical=2)),
                        ),
                    ],
                    spacing=4
                )
            ),
        ]) for idx, s in enumerate(soldiers_sorted)
    ]
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
                        columns=[
                            ft.DataColumn(label=ft.Text("Nr.", text_align=ft.TextAlign.LEFT), numeric=True),
                            ft.DataColumn(label=ft.Text("Dienstgrad", text_align=ft.TextAlign.LEFT)),
                            ft.DataColumn(label=ft.Text("Nachname", text_align=ft.TextAlign.LEFT)),
                            ft.DataColumn(label=ft.Text("Vorname", text_align=ft.TextAlign.LEFT)),
                            ft.DataColumn(label=ft.Text("Personalnummer", text_align=ft.TextAlign.LEFT)),
                            ft.DataColumn(label=ft.Text("Personenkennziffer", text_align=ft.TextAlign.LEFT)),
                            ft.DataColumn(label=ft.Text("Geburtsdatum", text_align=ft.TextAlign.LEFT)),
                            ft.DataColumn(label=ft.Text("Geburtsort", text_align=ft.TextAlign.LEFT)),
                            ft.DataColumn(label=ft.Text("Telefonnummer", text_align=ft.TextAlign.LEFT)),
                            ft.DataColumn(label=ft.Text("Aktion", text_align=ft.TextAlign.LEFT)),
                        ],
                        rows=table_rows,
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

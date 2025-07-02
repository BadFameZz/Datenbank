import flet as ft
from src.theme import get_theme
from src.views.sidebar import Sidebar
from src.db import get_all_soldiers
from src.military_ranks import (
    MARINE_DIENSTGRADE,
    HEER_LW_DIENSTGRADE,
    get_dienstgrad_rang,
    ist_marine_dienstgrad,
    get_alle_dienstgrade,
    dienstgrad_sort_key
)
from src.views.tables.simple_table import build_simple_content
from src.views.tables.personal_table import build_personal_table
from src.views.tables.dokumente_table import build_dokumente_table
from src.views.tables.igf_table import build_igf_table
from src.views.tables.fahrzeuge_table import build_fahrzeuge_table
from src.views.tables.atn_table import build_atn_table

def create_data_view(page: ft.Page):
    page.current_view = create_data_view
    theme = get_theme("dark" if page.theme_mode == ft.ThemeMode.DARK else "light")
    page.bgcolor = theme["bg"]

    # Sidebar erstellen
    sidebar = Sidebar(page, theme, lambda e: page.theme_mode == ft.ThemeMode.LIGHT, getattr(page, 'sidebar_collapsed', False)).get()

    # Header wie im Dashboard: padding=ft.padding.symmetric(horizontal=20), Row-Alignment identisch
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

    # Soldaten aus DB laden und sortieren
    soldiers = get_all_soldiers()
    soldiers_sorted = sorted(soldiers, key=dienstgrad_sort_key)

    def open_popup(soldat):
        def validate_fields():
            errors = []
            if not dienstgrad_dropdown.value:
                dienstgrad_dropdown.error_text = "Dienstgrad ist erforderlich"
                errors.append("Dienstgrad")
            if not name_field.value or len(name_field.value.strip()) == 0:
                name_field.error_text = "Nachname ist erforderlich"
                errors.append("Nachname")
            if not vorname_field.value or len(vorname_field.value.strip()) == 0:
                vorname_field.error_text = "Vorname ist erforderlich"
                errors.append("Vorname")
            page.update()
            return len(errors) == 0

        def clear_errors():
            dienstgrad_dropdown.error_text = None
            name_field.error_text = None
            vorname_field.error_text = None
            page.update()

        def close_sheet(e):
            edit_view.visible = False
            page.update()

        # Checkbox für Marine mit korrekter Erkennung des aktuellen Dienstgrad-Typs
        is_marine = ft.Checkbox(
            label="Dienstgrade: Marine",
            value=ist_marine_dienstgrad(soldat["dienstgrad"])
        )

        def update_dienstgrad_dropdown(e):
            if is_marine.value:
                dienstgrad_dropdown.options = [ft.dropdown.Option(dg) for dg in get_alle_dienstgrade(nur_marine=True)]
            else:
                dienstgrad_dropdown.options = [ft.dropdown.Option(dg) for dg in get_alle_dienstgrade(nur_heer_lw=True)]
            # Aktuelle Auswahl beibehalten, wenn möglich
            if dienstgrad_dropdown.value not in [opt.key for opt in dienstgrad_dropdown.options]:
                dienstgrad_dropdown.value = None
            page.update()

        is_marine.on_change = update_dienstgrad_dropdown

        # Dienstgrad-Dropdown mit initialen Optionen
        dienstgrad_dropdown = ft.Dropdown(
            label="Dienstgrad",
            hint_text="Dienstgrad wählen...",
            width=300,
            options=[ft.dropdown.Option(dg) for dg in (MARINE_DIENSTGRADE if is_marine.value else HEER_LW_DIENSTGRADE)],
            value=soldat["dienstgrad"],
            on_change=lambda _: clear_errors()
        )

        # Initial Marine-Status setzen
        if is_marine.value:
            update_dienstgrad_dropdown(None)

        name_field = ft.TextField(
            label="Nachname",
            value=soldat["name"],
            border=ft.InputBorder.UNDERLINE,
            width=300,
            on_change=lambda _: clear_errors()
        )
        vorname_field = ft.TextField(
            label="Vorname",
            value=soldat["vorname"],
            border=ft.InputBorder.UNDERLINE,
            width=300,
            on_change=lambda _: clear_errors()
        )
        personenkennziffer_field = ft.TextField(
            label="Personenkennziffer",
            value=soldat["personenkennziffer"] or "",
            border=ft.InputBorder.UNDERLINE,
            width=300,
            hint_text="Optional"
        )
        geburtsdatum_field = ft.TextField(
            label="Geburtsdatum",
            value=soldat["geburtsdatum"] or "",
            border=ft.InputBorder.UNDERLINE,
            width=300,
            hint_text="Optional (Format: TT.MM.JJJJ)"
        )
        geburtsort_field = ft.TextField(
            label="Geburtsort",
            value=soldat["geburtsort"] or "",
            border=ft.InputBorder.UNDERLINE,
            width=300,
            hint_text="Optional"
        )
        telefonnummer_field = ft.TextField(
            label="Telefonnummer",
            value=soldat["telefonnummer"] or "",
            border=ft.InputBorder.UNDERLINE,
            width=300,
            hint_text="Optional"
        )

        def save_changes(e):
            if not validate_fields():
                return

            try:
                import sqlite3
                from src.db import DB_NAME
                updated = dict(soldat)
                updated["dienstgrad"] = dienstgrad_dropdown.value
                updated["name"] = name_field.value.strip()
                updated["vorname"] = vorname_field.value.strip()
                updated["personenkennziffer"] = personenkennziffer_field.value.strip() or None
                updated["geburtsdatum"] = geburtsdatum_field.value.strip() or None
                updated["geburtsort"] = geburtsort_field.value.strip() or None
                updated["telefonnummer"] = telefonnummer_field.value.strip() or None

                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute('''
                    UPDATE soldiers SET dienstgrad=?, name=?, vorname=?, personenkennziffer=?, 
                    geburtsdatum=?, geburtsort=?, telefonnummer=? WHERE personalnummer=?
                ''', (
                    updated["dienstgrad"],
                    updated["name"],
                    updated["vorname"],
                    updated["personenkennziffer"],
                    updated["geburtsdatum"],
                    updated["geburtsort"],
                    updated["telefonnummer"],
                    updated["personalnummer"]
                ))
                conn.commit()
                conn.close()

                edit_view.visible = False
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Eintrag erfolgreich gespeichert!", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.GREEN_700
                )
                page.snack_bar.open = True
                page.update()
                page.clean()
                page.add(create_data_view(page))

            except sqlite3.Error as e:
                print(f"Datenbankfehler: {e}")
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Fehler beim Speichern!", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED_700
                )
                page.snack_bar.open = True
                page.update()

        # Container für die Bearbeitungsansicht
        edit_view = ft.Card(
            visible=True,
            elevation=10,
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Row([
                            ft.Text(
                                f"Soldat bearbeiten: {soldat['personalnummer']}", 
                                size=20, 
                                weight=ft.FontWeight.W_700,
                                expand=True
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                on_click=close_sheet
                            )
                        ]),
                        padding=ft.padding.only(bottom=20)
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Pflichtfelder", weight=ft.FontWeight.W_500, size=16),
                            is_marine,  # Marine-Checkbox hinzufügen
                            dienstgrad_dropdown,
                            name_field,
                            vorname_field,
                        ], spacing=10),
                        padding=ft.padding.symmetric(vertical=10)
                    ),
                    ft.Divider(),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Optionale Felder", weight=ft.FontWeight.W_500, size=16),
                            personenkennziffer_field,
                            geburtsdatum_field,
                            geburtsort_field,
                            telefonnummer_field
                        ], spacing=10),
                        padding=ft.padding.symmetric(vertical=10)
                    ),
                    ft.Container(
                        content=ft.Row([
                            ft.TextButton(
                                "Abbrechen",
                                on_click=close_sheet
                            ),
                            ft.ElevatedButton(
                                "Speichern",
                                on_click=save_changes
                            )
                        ], alignment=ft.MainAxisAlignment.END),
                        padding=ft.padding.only(top=20)
                    )
                ]),
                padding=ft.padding.all(20),
                width=400  # Feste Breite für besseres Layout
            )
        )
        
        # Container zur Seite hinzufügen
        overlay = ft.Stack([
            edit_view
        ])
        page.overlay.append(overlay)
        page.update()

    def delete_soldier(soldat):
        def close_dlg(e):
            dlg_modal.open = False
            page.update()

        def confirm_delete(e):
            from src.db import delete_soldier as db_delete_soldier
            print(f"Lösche Soldat mit Personalnummer: {soldat['personalnummer']}")
            print("Starte Löschvorgang in der Datenbank...")
            success = db_delete_soldier(soldat["personalnummer"])
            if success:
                print("Löschen erfolgreich. Aktualisiere die Ansicht...")
            else:
                print("Fehler beim Löschen des Eintrags in der Datenbank.")
            delete_view.visible = False
            page.update()
            if success:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Soldat {soldat['dienstgrad']} {soldat['name']} wurde gelöscht", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.GREEN_700
                )
                page.snack_bar.open = True
                page.update()
                page.clean()
                page.add(create_data_view(page))
            else:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Fehler beim Löschen!", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED_700
                )
                page.snack_bar.open = True
                page.update()

        # Container für die Löschansicht
        delete_view = ft.Card(
            visible=True,
            elevation=10,
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Row([
                            ft.Text(
                                f"Soldat löschen: {soldat['personalnummer']}",
                                size=20,
                                weight=ft.FontWeight.W_700,
                                expand=True
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                on_click=lambda e: (setattr(delete_view, 'visible', False), page.update())
                            )
                        ]),
                        padding=ft.padding.only(bottom=20)
                    ),
                    ft.Text(f"Möchten Sie {soldat['dienstgrad']} {soldat['name']} wirklich löschen?", color=theme["text"]),
                    ft.Container(
                        content=ft.Row([
                            ft.TextButton(
                                "Abbrechen",
                                on_click=lambda e: (setattr(delete_view, 'visible', False), page.update())
                            ),
                            ft.ElevatedButton(
                                "Löschen",
                                color=ft.Colors.WHITE,
                                bgcolor=ft.Colors.RED_500,
                                on_click=lambda e: confirm_delete(e)
                            )
                        ], alignment=ft.MainAxisAlignment.END),
                        padding=ft.padding.only(top=20)
                    )
                ]),
                padding=ft.padding.all(20),
                width=400
            )
        )

        # Overlay anzeigen
        overlay = ft.Stack([
            delete_view
        ])
        page.overlay.append(overlay)
        page.update()

    # Persönliche Daten Tabelle (mit Aktionen)
    main_content = build_personal_table(soldiers_sorted, theme, page, open_popup, delete_soldier)

    # Tabs setzen
    tab_controller = ft.Tabs(
        selected_index=0,
        animation_duration=200,
        tabs=[
            ft.Tab(text="Persönliche Daten", content=main_content),
            ft.Tab(text="Dokumente", content=build_dokumente_table(soldiers_sorted, theme, page)),
            ft.Tab(text="IGF", content=build_igf_table(soldiers_sorted, theme, page)),
            ft.Tab(text="Fahrzeuge", content=build_fahrzeuge_table(soldiers_sorted, theme, page)),
            ft.Tab(text="ATN", content=build_atn_table(soldiers_sorted, theme, page)),
        ]
    )

    # Äußeres Layout erstellen (Tabs einbinden)
    layout = ft.Row([
        sidebar,
        ft.Column([
            header,
            tab_controller
        ], expand=True)
    ], spacing=0, expand=True)

    # Seite leeren und Layout hinzufügen
    page.clean()
    page.add(layout)
    page.update()
    return layout  # Layout zurückgeben

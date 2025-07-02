import flet as ft
from src.theme import get_theme
from src.views.sidebar import Sidebar
from src.db import insert_soldier

def create_add_soldier_view(page: ft.Page):
    page.current_view = create_add_soldier_view
    theme = get_theme("dark" if page.theme_mode == ft.ThemeMode.DARK else "light")

    # Mannschaftsdienstgrade (identisch für alle TSK)
    mannschaft_dienstgrade = [
        "Gefreiter",
        "Obergefreiter",
        "Hauptgefreiter",
        "Stabsgefreiter",
        "Oberstabsgefreiter",
        "Korporal",
        "Stabskorporal"
    ]
    # Heer/Luftwaffe spezifisch
    heer_lw_dienstgrade = mannschaft_dienstgrade + [
        "Unteroffizier",
        "Fahnenjunker",
        "Stabsunteroffizier",
        "Feldwebel",
        "Fähnrich",
        "Oberfeldwebel",
        "Hauptfeldwebel",
        "Oberfähnrich",
        "Stabsfeldwebel",
        "Oberstabsfeldwebel",
        "Leutnant",
        "Oberleutnant",
        "Hauptmann",
        "Stabshauptmann",
        "Major",
        "Oberstleutnant",
        "Oberst",
        "Brigadegeneral",
        "Generalmajor",
        "Generalleutnant",
        "General"
    ]
    # Marine spezifisch (ohne Mannschaftsdienstgrade)
    marine_dienstgrade = mannschaft_dienstgrade + [
        "Maat",
        "Seekadett",
        "Obermaat",
        "Bootsmann",
        "Fähnrich zur See",
        "Oberbootsmann",
        "Hauptbootsmann",
        "Oberfähnrich zur See",
        "Stabsbootsmann",
        "Oberstabsbootsmann",
        "Leutnant zur See",
        "Oberleutnant zur See",
        "Kapitänleutnant",
        "Stabskapitänleutnant",
        "Korvettenkapitän",
        "Fregattenkapitän",
        "Kapitän zur See",
        "Flottillenadmiral",
        "Konteradmiral",
        "Vizeadmiral",
        "Admiral"
    ]

    # Checkbox für Marine
    is_marine = ft.Checkbox(label="Dienstgrade: Marine", value=False)

    def update_dienstgrad_dropdown(e):
        if is_marine.value:
            dienstgrad_dropdown.options = [ft.dropdown.Option(dg) for dg in marine_dienstgrade]
        else:
            dienstgrad_dropdown.options = [ft.dropdown.Option(dg) for dg in heer_lw_dienstgrade]
        page.update()

    is_marine.on_change = update_dienstgrad_dropdown

    dienstgrad_dropdown = ft.Dropdown(
        label="Dienstgrad",
        hint_text="Dienstgrad wählen...",
        options=[ft.dropdown.Option(dg) for dg in heer_lw_dienstgrade],
        autofocus=True,
        width=400,
    )

    name_field = ft.TextField(label="Nachname*", width=400)
    vorname_field = ft.TextField(label="Vorname*", width=400)
    personalnummer_field = ft.TextField(label="Personalnummer*", width=400)
    personenkennziffer_field = ft.TextField(label="Personenkennziffer", width=400)
    geburtsdatum_field = ft.TextField(label="Geburtsdatum (TT.MM.JJJJ)", width=400, hint_text="z.B. 19.05.1990")
    geburtsort_field = ft.TextField(label="Geburtsort", width=400)
    telefonnummer_field = ft.TextField(label="Telefonnummer", width=400)

    def speichern(e):
        errors = []
        if not dienstgrad_dropdown.value:
            errors.append("Dienstgrad ist ein Pflichtfeld.")
        if not name_field.value:
            errors.append("Nachname ist ein Pflichtfeld.")
        if not vorname_field.value:
            errors.append("Vorname ist ein Pflichtfeld.")
        if not personalnummer_field.value:
            errors.append("Personalnummer ist ein Pflichtfeld.")
        if errors:
            page.snack_bar = ft.SnackBar(ft.Text(" ".join(errors), color=ft.Colors.RED))
            page.snack_bar.open = True
            page.update()
            return
        # Soldat speichern
        try:
            insert_soldier({
                "personalnummer": personalnummer_field.value,
                "dienstgrad": dienstgrad_dropdown.value,
                "name": name_field.value,
                "vorname": vorname_field.value,
                "personenkennziffer": personenkennziffer_field.value,
                "geburtsdatum": geburtsdatum_field.value,
                "geburtsort": geburtsort_field.value,
                "telefonnummer": telefonnummer_field.value,
                "marine": is_marine.value
            })
            page.snack_bar = ft.SnackBar(ft.Text("Soldat gespeichert!", color=ft.Colors.GREEN))
            # Optional: Felder leeren
            dienstgrad_dropdown.value = None
            name_field.value = ""
            vorname_field.value = ""
            personalnummer_field.value = ""
            personenkennziffer_field.value = ""
            geburtsdatum_field.value = ""
            geburtsort_field.value = ""
            telefonnummer_field.value = ""
            is_marine.value = False
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Fehler beim Speichern: {ex}", color=ft.Colors.RED))
        page.snack_bar.open = True
        page.update()

    def go_back(e):
        from src.views.dashboard_view import create_dashboard_view
        page.clean()
        page.add(create_dashboard_view(page))

    # Modernes Card-Design für das Formular mit sinnvoller Anordnung
    form_card = ft.Container(
        bgcolor=theme["sidebar"],
        border_radius=ft.border_radius.all(16),
        padding=ft.padding.only(left=40, right=40, top=24, bottom=24),
        shadow=ft.BoxShadow(
            color="#00000022",
            blur_radius=16,
            offset=ft.Offset(0, 4)
        ),
        alignment=ft.alignment.center,
        content=ft.Column([
            ft.Text("Persönliche Daten", size=20, weight=ft.FontWeight.BOLD, color=theme["text"]),
            ft.Divider(height=16, color=theme["sidebar_divider"]),
            is_marine,
            ft.Row([
                dienstgrad_dropdown,
                name_field,
                vorname_field
            ], spacing=24, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Row([
                personalnummer_field,
                personenkennziffer_field
            ], spacing=24, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Row([
                geburtsdatum_field,
                geburtsort_field,
                telefonnummer_field
            ], spacing=24, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Row([
                ft.ElevatedButton("Speichern", icon=ft.Icons.SAVE, bgcolor=theme["button"], color=theme["button_text"], on_click=speichern),
                ft.TextButton("Abbrechen", on_click=go_back)
            ], alignment=ft.MainAxisAlignment.START, spacing=10)
        ], spacing=18, horizontal_alignment=ft.CrossAxisAlignment.START)
    )

    sidebar = Sidebar(page, theme, lambda e: page.theme_mode == ft.ThemeMode.LIGHT, getattr(page, 'sidebar_collapsed', False)).get()

    # Header wie im Dashboard
    header = ft.Container(
        height=60,
        bgcolor=theme["header"],
        padding=ft.padding.symmetric(horizontal=20),
        content=ft.Row([
            ft.IconButton(
                icon=ft.Icons.MENU,
                icon_color="#ffffff",
                on_click=lambda e: setattr(page, 'sidebar_collapsed', not getattr(page, 'sidebar_collapsed', False)) or page.clean() or page.add(create_add_soldier_view(page)),
            ),
            ft.Text("Soldat hinzufügen", size=24, weight=ft.FontWeight.BOLD, color="#ffffff", expand=True),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

    # Content-Bereich mit mittiger Card
    main_content = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        padding=ft.padding.all(20),
        content=form_card
    )

    layout = ft.Row([
        sidebar,
        ft.Column([
            header,
            main_content,
        ], expand=True)
    ], spacing=0, expand=True)

    return layout

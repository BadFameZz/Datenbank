"""
Dieses Modul enthält alle Definitionen und Funktionen für die Handhabung von militärischen Dienstgraden.
Es unterstützt sowohl Heer/Luftwaffe als auch Marine-Dienstgrade und bietet Funktionen für:
- Dienstgrad-Validierung
- Sortierung nach Rangfolge
- Äquivalenz-Prüfung zwischen Marine und Heer/Luftwaffe
"""

# Dienstgrade nach Kategorien definieren
MANNSCHAFT_DIENSTGRADE = [
    "Gefreiter",
    "Obergefreiter",
    "Hauptgefreiter",
    "Stabsgefreiter",
    "Oberstabsgefreiter",
    "Korporal",
    "Stabskorporal"
]

HEER_LW_DIENSTGRADE = MANNSCHAFT_DIENSTGRADE + [
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

MARINE_DIENSTGRADE = MANNSCHAFT_DIENSTGRADE + [
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

# Dienstgrad-Rangfolge für Sortierung (niedrigster zuerst)
DIENSTGRAD_RANKING = [
    # Mannschaftsdienstgrade (Heer/Luftwaffe und Marine gleich)
    "Gefreiter", "Obergefreiter", "Hauptgefreiter", "Stabsgefreiter", "Oberstabsgefreiter", "Korporal", "Stabskorporal",
    
    # Unteroffiziere ohne Portepee
    "Unteroffizier",         # Heer/Luftwaffe
    "Maat",                  # Marine (equivalent zu Unteroffizier)
    "Seekadett",             # Marine
    "Fahnenjunker",          # Heer/Luftwaffe
    "Stabsunteroffizier",    # Heer/Luftwaffe
    "Obermaat",              # Marine (equivalent zu Stabsunteroffizier)
    
    # Unteroffiziere mit Portepee
    "Feldwebel",             # Heer/Luftwaffe
    "Bootsmann",             # Marine (equivalent zu Feldwebel)
    "Fähnrich",             # Heer/Luftwaffe
    "Fähnrich zur See",      # Marine
    "Oberfeldwebel",         # Heer/Luftwaffe
    "Oberbootsmann",         # Marine (equivalent zu Oberfeldwebel)
    "Hauptfeldwebel",        # Heer/Luftwaffe
    "Hauptbootsmann",        # Marine (equivalent zu Hauptfeldwebel)
    "Oberfähnrich",          # Heer/Luftwaffe
    "Oberfähnrich zur See",  # Marine
    "Stabsfeldwebel",        # Heer/Luftwaffe
    "Stabsbootsmann",        # Marine (equivalent zu Stabsfeldwebel)
    "Oberstabsfeldwebel",    # Heer/Luftwaffe
    "Oberstabsbootsmann",    # Marine (equivalent zu Oberstabsfeldwebel)
    
    # Leutnante
    "Leutnant",              # Heer/Luftwaffe
    "Leutnant zur See",      # Marine
    "Oberleutnant",          # Heer/Luftwaffe
    "Oberleutnant zur See",  # Marine
    
    # Hauptleute
    "Hauptmann",             # Heer/Luftwaffe
    "Kapitänleutnant",       # Marine (equivalent zu Hauptmann)
    "Stabshauptmann",        # Heer/Luftwaffe
    "Stabskapitänleutnant",  # Marine (equivalent zu Stabshauptmann)
    
    # Stabsoffiziere
    "Major",                 # Heer/Luftwaffe
    "Korvettenkapitän",      # Marine (equivalent zu Major)
    "Oberstleutnant",        # Heer/Luftwaffe
    "Fregattenkapitän",      # Marine (equivalent zu Oberstleutnant)
    "Oberst",                # Heer/Luftwaffe
    "Kapitän zur See",       # Marine (equivalent zu Oberst)
    
    # Generäle/Admirale
    "Brigadegeneral",        # Heer/Luftwaffe
    "Flottillenadmiral",     # Marine (equivalent zu Brigadegeneral)
    "Generalmajor",          # Heer/Luftwaffe
    "Konteradmiral",         # Marine (equivalent zu Generalmajor)
    "Generalleutnant",       # Heer/Luftwaffe
    "Vizeadmiral",           # Marine (equivalent zu Generalleutnant)
    "General",               # Heer/Luftwaffe
    "Admiral"                # Marine (equivalent zu General)
]

DIENSTGRAD_RANKING_MAP = {dg: i for i, dg in enumerate(DIENSTGRAD_RANKING)}

def dienstgrad_sort_key(soldat):
    """
    Sortiert Soldaten nach Dienstgrad (höchster zuerst) und dann nach Name
    """
    # Je höher der Index, desto niedriger der Rang, daher mit negativem Vorzeichen für umgekehrte Sortierung
    return -DIENSTGRAD_RANKING_MAP.get(soldat["dienstgrad"], 0), soldat["name"].lower()

def ist_marine_dienstgrad(dienstgrad):
    """
    Prüft, ob ein Dienstgrad ein Marine-Dienstgrad ist.
    
    Args:
        dienstgrad (str): Der zu prüfende Dienstgrad
        
    Returns:
        bool: True wenn es ein Marine-Dienstgrad ist, sonst False
    """
    return dienstgrad in MARINE_DIENSTGRADE

def ist_heer_lw_dienstgrad(dienstgrad):
    """
    Prüft, ob ein Dienstgrad ein Heer/Luftwaffen-Dienstgrad ist.
    
    Args:
        dienstgrad (str): Der zu prüfende Dienstgrad
        
    Returns:
        bool: True wenn es ein Heer/Luftwaffen-Dienstgrad ist, sonst False
    """
    return dienstgrad in HEER_LW_DIENSTGRADE

def get_aequivalenten_dienstgrad(dienstgrad, zu_marine=True):
    """
    Gibt den äquivalenten Dienstgrad in der anderen Kategorie zurück (Marine zu Heer/Luftwaffe oder umgekehrt).
    
    Args:
        dienstgrad (str): Der umzuwandelnde Dienstgrad
        zu_marine (bool): True wenn in Marine-Dienstgrad konvertiert werden soll, 
                         False für Konvertierung zu Heer/Luftwaffe
    
    Returns:
        str: Der äquivalente Dienstgrad oder None wenn keine Entsprechung gefunden wird
    """
    # Mannschaftsdienstgrade sind identisch
    if dienstgrad in MANNSCHAFT_DIENSTGRADE:
        return dienstgrad
        
    # Äquivalenz-Map definieren (Heer/Luftwaffe -> Marine)
    aequivalenzen = {
        "Unteroffizier": "Maat",
        "Stabsunteroffizier": "Obermaat",
        "Feldwebel": "Bootsmann",
        "Oberfeldwebel": "Oberbootsmann",
        "Hauptfeldwebel": "Hauptbootsmann",
        "Stabsfeldwebel": "Stabsbootsmann",
        "Oberstabsfeldwebel": "Oberstabsbootsmann",
        "Leutnant": "Leutnant zur See",
        "Oberleutnant": "Oberleutnant zur See",
        "Hauptmann": "Kapitänleutnant",
        "Stabshauptmann": "Stabskapitänleutnant",
        "Major": "Korvettenkapitän",
        "Oberstleutnant": "Fregattenkapitän",
        "Oberst": "Kapitän zur See",
        "Brigadegeneral": "Flottillenadmiral",
        "Generalmajor": "Konteradmiral",
        "Generalleutnant": "Vizeadmiral",
        "General": "Admiral"
    }
    
    # Für Konvertierung zu Heer/Luftwaffe die Map umkehren
    if not zu_marine:
        aequivalenzen = {v: k for k, v in aequivalenzen.items()}
    
    return aequivalenzen.get(dienstgrad)

def get_dienstgrad_rang(dienstgrad):
    """
    Gibt den numerischen Rang eines Dienstgrads zurück (höherer Wert = höherer Rang).
    
    Args:
        dienstgrad (str): Der Dienstgrad
        
    Returns:
        int: Der numerische Rang oder -1 wenn der Dienstgrad unbekannt ist
    """
    return DIENSTGRAD_RANKING_MAP.get(dienstgrad, -1)

def get_alle_dienstgrade(nur_marine=False, nur_heer_lw=False):
    """
    Gibt alle verfügbaren Dienstgrade zurück, optional gefiltert nach Kategorie.
    
    Args:
        nur_marine (bool): Wenn True, nur Marine-Dienstgrade zurückgeben
        nur_heer_lw (bool): Wenn True, nur Heer/Luftwaffen-Dienstgrade zurückgeben
        
    Returns:
        list: Liste der Dienstgrade, sortiert nach Rang (niedrigster zuerst)
    """
    if nur_marine:
        return MARINE_DIENSTGRADE
    elif nur_heer_lw:
        return HEER_LW_DIENSTGRADE
    else:
        return sorted(set(MARINE_DIENSTGRADE + HEER_LW_DIENSTGRADE),
                     key=lambda x: DIENSTGRAD_RANKING_MAP.get(x, 0))

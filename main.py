import sys
import time
import random
import os

# --- FARBEN & DESIGN ---
class F:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BG_BLUE = "\033[44m"

# --- HAUS-GENERATOR (DYNAMISCH) ---
def get_house_art(preis, name):
    """Erstellt ein einzigartiges Haus basierend auf Preis und Name"""
    letter = name[0].upper() # Der erste Buchstabe der Straße
    
    # TYP 1: Die Bruchbude (Billig: Preis 1-3)
    if preis <= 3:
        return [
            "        ",
            "   /\\   ",
            "  /  \\  ",
            f" | {letter}  | ", # Mit Buchstabe!
            " |____| "
        ]
    
    # TYP 2: Das Familienhaus (Mittel: Preis 4-6)
    elif preis <= 6:
        return [
            "   /\\   ",
            "  /  \\  ",
            " /____\\ ",
            f" | {letter}  | ",
            " |____| "
        ]
    
    # TYP 3: Die Luxus-Villa (Teuer: Preis 7+)
    else:
        return [
            " _/||\\_ ", # Episches Dach
            "/______\\",
            "|  ==  |",
            f"|  {letter}{letter}  |", # Doppeltür
            "|______|"
        ]

# --- SYSTEM-TOOLS ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def typewriter(text, speed=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def linie():
    print(F.CYAN + "═" * 50 + F.RESET)

# --- DATEN ---
TOKENS = ["🍺", "🍷", "🥃", "🍸", "🍹", "🧉"]

BOARD = [
    {"name": "LOS (Start)", "typ": "start", "color": F.WHITE},
    {"name": "Pfeffi-Gasse", "typ": "str", "preis": 2, "color": F.MAGENTA, "owner": None},
    {"name": "Klopfer-Weg", "typ": "str", "preis": 2, "color": F.MAGENTA, "owner": None},
    {"name": "BAR (Ereignis)", "typ": "event", "color": F.WHITE},
    {"name": "Radler-Ring", "typ": "str", "preis": 3, "color": F.CYAN, "owner": None},
    {"name": "Bier-Bahnhof", "typ": "bahn", "preis": 4, "color": F.WHITE, "owner": None},
    {"name": "Pils-Promenade", "typ": "str", "preis": 3, "color": F.CYAN, "owner": None},
    {"name": "Kater-Chance", "typ": "event", "color": F.WHITE},
    {"name": "Wein-Weg", "typ": "str", "preis": 4, "color": F.MAGENTA, "owner": None},
    {"name": "Rosé-Platz", "typ": "str", "preis": 4, "color": F.MAGENTA, "owner": None},
    {"name": "GEFÄNGNIS", "typ": "jail", "color": F.RED},
    {"name": "Aperol-Allee", "typ": "str", "preis": 5, "color": F.YELLOW, "owner": None},
    {"name": "Sekt-Straße", "typ": "str", "preis": 5, "color": F.YELLOW, "owner": None},
    {"name": "U-Bahn", "typ": "bahn", "preis": 4, "color": F.WHITE, "owner": None},
    {"name": "Jägermeister-Eck", "typ": "str", "preis": 6, "color": F.GREEN, "owner": None},
    {"name": "Absinth-Abgrund", "typ": "str", "preis": 6, "color": F.GREEN, "owner": None},
    {"name": "FREI PARKEN", "typ": "park", "color": F.WHITE},
    {"name": "Gin-Gasse", "typ": "str", "preis": 7, "color": F.BLUE, "owner": None},
    {"name": "Rum-Runde", "typ": "str", "preis": 7, "color": F.BLUE, "owner": None},
    {"name": "Taxi-Zentrale", "typ": "bahn", "preis": 4, "color": F.WHITE, "owner": None},
    {"name": "STEUER (Trink!)", "typ": "tax", "color": F.WHITE},
    {"name": "Tequila-Traum", "typ": "str", "preis": 8, "color": F.RED, "owner": None},
    {"name": "RISIKO", "typ": "event", "color": F.WHITE},
    {"name": "Vodka-Villa", "typ": "str", "preis": 10, "color": F.BLUE, "owner": None},
]

TASKS = [
    "Alle trinken einen Schluck.",
    "Der Kleinste in der Runde trinkt 2.",
    "Reimrunde: Reime auf 'Saufen'.",
    "Verteile 3 Schlücke."
]

# --- KLASSEN ---
class Spieler:
    def __init__(self, name, token, pid):
        self.name = name
        self.token = token
        self.id = pid
        self.pos = 0
        self.besitz = []

# --- AUKTIONS-FUNKTION ---
def starte_auktion(feld, spieler_liste, aktueller_spieler):
    print(f"\n{F.YELLOW}🔨 AUKTION GESTARTET! 🔨{F.RESET}")
    print(f"Niemand wollte {feld['name']} zum Normalpreis.")
    print("Wer bereit ist, am meisten zu trinken, bekommt die Straße!")
    
    hoechstgebot = 0
    hoechnstbietender = None
    
    for s in spieler_liste:
        if s == aktueller_spieler: continue 
        
        try:
            gebot_str = input(f"{s.name} ({s.token}), wie viele Schlücke bietest du? (0 = raus) >> ")
            gebot = int(gebot_str) if gebot_str.isdigit() else 0
        except:
            gebot = 0
            
        if gebot > hoechstgebot:
            hoechstgebot = gebot
            hoechnstbietender = s
            print(f"-> {F.GREEN}Neues Höchstgebot: {gebot} Schlücke!{F.RESET}")
    
    if hoechnstbietender:
        print(f"\n{F.BOLD}Verkauft an {hoechnstbietender.name} für {hoechstgebot} Schlücke!{F.RESET}")
        print("TRINK JETZT!")
        time.sleep(2)
        feld["owner"] = hoechnstbietender
        hoechnstbietender.besitz.append(feld)
    else:
        print("Keiner will es? Dann bleibt es bei der Bank.")

# --- GRAFIK FUNKTIONEN ---
def draw_card(feld, spieler):
    c = feld["color"]
    r = F.RESET
    w = 42
    
    print(f"\n{c}╔{'═'*w}╗{r}")
    
    # Titel Zeile
    content = f" {feld['name']} "
    space = w - len(content)
    print(f"{c}║{r}" + (" " * (space//2)) + F.BOLD + content + F.RESET + (" " * (space - space//2)) + f"{c}║{r}")
    print(f"{c}╠{'═'*w}╣{r}")
    
    # --- DYNAMISCHES HAUS LOGIK ---
    if "owner" in feld and feld["owner"] is not None:
        besitzer_name = feld["owner"].name
        
        # Hier holen wir uns das einzigartige Haus für diese Straße
        house_art = get_house_art(feld.get("preis", 0), feld["name"])
        
        for i, line in enumerate(house_art):
            # Text links, Haus rechts
            text_part = ""
            if i == 1: text_part = f"BESITZER:"
            if i == 2: text_part = f"{besitzer_name[:12]}" # Namen kürzen falls zu lang
            
            # Formatiertes Haus rechtsbündig einfügen
            print(f"{c}║{r} {text_part:<20} {F.YELLOW}{line:<10}{r}       {c}║{r}")
            
    else:
        # Standard Ansicht (Kein Haus)
        lines = []
        if feld["typ"] == "str" or feld["typ"] == "bahn":
            lines.append(f"PREIS: {feld['preis']} Schlücke")
            lines.append("(Noch zu haben!)")
        elif feld["typ"] == "event":
            lines.append("ZIEHE EINE KARTE...")
        else:
            lines.append(feld.get("aktion", ""))
            
        for line in lines:
            print(f"{c}║{r} {line:<{w-2}} {c}║{r}")
        for _ in range(5 - len(lines)): 
            print(f"{c}║{' ' * w}║{r}")

    print(f"{c}╚{'═'*w}╝{r}")
    print(f"   {spieler.token} {spieler.name} ist hier.\n")

# --- MAIN ENGINE ---
def spiel_starten():
    clear()
    print(f"{F.YELLOW}--- SAUF-MONOPOLY V4.0 (Custom Houses) ---{F.RESET}")
    
    try:
        anzahl = int(input("Anzahl Spieler (2-6): "))
    except:
        anzahl = 2
        
    spieler_liste = []
    for i in range(anzahl):
        token = TOKENS[i % len(TOKENS)]
        print(f"Name Spieler {i+1}:")
        name = input(f"({token}) >> ")
        if not name: name = f"Spieler {i+1}"
        spieler_liste.append(Spieler(name, token, i))
    
    running = True
    
    while running:
        for spieler in spieler_liste:
            clear()
            print(f"{F.BG_BLUE}{F.WHITE} {spieler.name} ist dran {F.RESET}")
            input(">> [ENTER] würfeln")
            
            # Würfeln
            wurf = random.randint(1, 6)
            print(f"🎲 Du hast eine {F.BOLD}{wurf}{F.RESET} gewürfelt.")
            time.sleep(0.5)
            
            spieler.pos = (spieler.pos + wurf) % len(BOARD)
            aktuelles_feld = BOARD[spieler.pos]
            
            # Karte zeichnen (Mit dynamischem Haus!)
            draw_card(aktuelles_feld, spieler)
            
            # Logik
            typ = aktuelles_feld["typ"]
            
            if typ == "str" or typ == "bahn":
                if aktuelles_feld["owner"] is None:
                    print(f"Kaufen für {aktuelles_feld['preis']} Schlücke? (j/n)")
                    wahl = input(">> ").lower()
                    
                    if wahl == "j":
                        print(f"{F.GREEN}GEKAUFT! Trink aus!{F.RESET}")
                        aktuelles_feld["owner"] = spieler
                        spieler.besitz.append(aktuelles_feld)
                    else:
                        starte_auktion(aktuelles_feld, spieler_liste, spieler)
                        
                elif aktuelles_feld["owner"] == spieler:
                    print("Dein Eigentum. Entspann dich.")
                else:
                    miete = aktuelles_feld['preis']
                    print(f"{F.RED}MIETE FÄLLIG!{F.RESET} Trinke {miete} Schlücke.")
            
            elif typ == "event":
                print(f"🃏 {random.choice(TASKS)}")
                
            input("\n[ENTER] Weiter...")

if __name__ == "__main__":
    spiel_starten()

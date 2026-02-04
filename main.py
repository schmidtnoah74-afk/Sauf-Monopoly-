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
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_BLUE = "\033[44m"

# --- SYSTEM-TOOLS ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def typewriter(text, speed=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def print_centered(text, width=50):
    print(text.center(width))

def linie():
    print(F.CYAN + "═" * 50 + F.RESET)

# --- DATEN: DAS BOARD ---
# Wir nutzen Icons für die Figuren
TOKENS = ["🍺", "🍷", "🥃", "🍸", "🍹", "🧉"]

# Das Spielfeld (24 Felder für gute Spielbarkeit)
BOARD = [
    {"name": "LOS (Start)", "typ": "start", "color": F.WHITE},
    {"name": "Pfeffi-Gasse", "typ": "str", "preis": 2, "color": F.MAGENTA},
    {"name": "Klopfer-Weg", "typ": "str", "preis": 2, "color": F.MAGENTA},
    {"name": "BAR (Ereignis)", "typ": "event", "color": F.WHITE},
    {"name": "Radler-Ring", "typ": "str", "preis": 3, "color": F.CYAN},
    {"name": "Bier-Bahnhof", "typ": "bahn", "preis": 4, "color": F.WHITE},
    {"name": "Pils-Promenade", "typ": "str", "preis": 3, "color": F.CYAN},
    {"name": "Kater-Chance", "typ": "event", "color": F.WHITE},
    {"name": "Wein-Weg", "typ": "str", "preis": 4, "color": F.MAGENTA},
    {"name": "Rosé-Platz", "typ": "str", "preis": 4, "color": F.MAGENTA},
    {"name": "GEFÄNGNIS", "typ": "jail", "color": F.RED},
    {"name": "Aperol-Allee", "typ": "str", "preis": 5, "color": F.YELLOW},
    {"name": "Sekt-Straße", "typ": "str", "preis": 5, "color": F.YELLOW},
    {"name": "U-Bahn", "typ": "bahn", "preis": 4, "color": F.WHITE},
    {"name": "Jägermeister-Eck", "typ": "str", "preis": 6, "color": F.GREEN},
    {"name": "Absinth-Abgrund", "typ": "str", "preis": 6, "color": F.GREEN},
    {"name": "FREI PARKEN", "typ": "park", "color": F.WHITE},
    {"name": "Gin-Gasse", "typ": "str", "preis": 7, "color": F.BLUE},
    {"name": "Rum-Runde", "typ": "str", "preis": 7, "color": F.BLUE},
    {"name": "Taxi-Zentrale", "typ": "bahn", "preis": 4, "color": F.WHITE},
    {"name": "STEUER (Trink!)", "typ": "tax", "color": F.WHITE},
    {"name": "Tequila-Traum", "typ": "str", "preis": 8, "color": F.RED},
    {"name": "RISIKO", "typ": "event", "color": F.WHITE},
    {"name": "Vodka-Villa", "typ": "str", "preis": 10, "color": F.BLUE},
]

TASKS_18 = [
    "Wahrheit: Wen aus der Runde findest du am attraktivsten? Oder trinke 5.",
    "Pflicht: Lass jemanden eine Nachricht an einen Kontakt deiner Wahl schreiben.",
    "Körperkontakt: Setze dich für eine Runde auf den Schoß deines linken Nachbarn.",
    "Strip-Light: Lege ein Teil ab oder exe dein Glas."
]

TASKS_16 = [
    "Alle trinken einen Schluck.",
    "Kategorie: Biermarken. Wer nichts weiß, trinkt.",
    "Reimrunde: Reime auf 'Saufen'.",
    "Verteile 5 Schlücke."
]

# --- KLASSEN ---
class Spieler:
    def __init__(self, name, token):
        self.name = name
        self.token = token
        self.pos = 0
        self.besitz = []
        self.gefaengnis = False

# --- GRAFIK FUNKTIONEN ---
def draw_card(feld, spieler):
    """Zeichnet eine schöne Karte des aktuellen Feldes"""
    c = feld["color"]
    r = F.RESET
    w = 40
    
    print(f"\n{c}╔{'═'*w}╗{r}")
    
    # Name zentriert
    content = f" {feld['name']} "
    space = w - len(content)
    print(f"{c}║{r}" + (" " * (space//2)) + F.BOLD + content + F.RESET + (" " * (space - space//2)) + f"{c}║{r}")
    
    print(f"{c}╠{'═'*w}╣{r}")
    
    # Details je nach Typ
    lines = []
    if feld["typ"] == "str":
        besitzer = "Niemand"
        # Check owner logic later
        lines.append(f"PREIS: {feld['preis']} Schlücke")
        lines.append(" ")
        lines.append("Ein Haus kaufen?")
    elif feld["typ"] == "start":
        lines.append("Hole dir 2 Schlücke ab!")
    elif feld["typ"] == "event":
        lines.append("Ziehe eine Karte...")
        lines.append("???")
    else:
        lines.append(feld.get("aktion", "Nichts passiert."))

    # Inhalt füllen
    for line in lines:
        l_len = len(line) # Achtung: Farben zählen nicht zur Länge, hier vereinfacht
        print(f"{c}║{r} {line:<{w-2}} {c}║{r}")
        
    # Leere Zeilen auffüllen
    for _ in range(4 - len(lines)):
         print(f"{c}║{' ' * w}║{r}")

    # Footer mit Spieler
    print(f"{c}╚{'═'*w}╝{r}")
    print(f"   {spieler.token} {spieler.name} ist hier gelandet.\n")

def animierter_wuerfel():
    print("🎲 Würfel rollt...", end="")
    for _ in range(3):
        time.sleep(0.2)
        sys.stdout.write(".")
        sys.stdout.flush()
    val = random.randint(1, 6)
    print(f" {F.BOLD}{F.YELLOW}{val}!{F.RESET}")
    return val

# --- MAIN ENGINE ---
def spiel_starten():
    clear()
    print(f"{F.YELLOW}")
    print("  __  __  ____  _   _  ____  _____  ____  __  __   __ ")
    print(" |  \/  |/ __ \| \ | |/ __ \|  __ \| __ \|  \/  | |  |")
    print(" | \  / | |  | |  \| | |  | | |__) | |  | | \  / | |  |")
    print(" | |\/| | |  | | . ` | |  | |  ___/| |  | | |\/| | |  |")
    print(" | |  | | |__| | |\  | |__| | |    | |__| | |  | | |__|")
    print(" |_|  |_|\____/|_| \_|\____/|_|    |_____/|_|  |_| (__)  ")
    print(f"{F.RESET}")
    print("       Die ultimative Sauf-Edition v3.0 (Visual)")
    linie()
    
    # 1. SETUP
    print("Wie viele Leute saufen mit? (2-6)")
    try:
        anzahl = int(input(">> "))
    except:
        anzahl = 2
    
    print("\nModus? [1] Party (16+) | [2] Eskalation (18+)")
    modus_wahl = input(">> ")
    kartenstapel = TASKS_18 if modus_wahl == "2" else TASKS_16
    
    spieler_liste = []
    
    for i in range(anzahl):
        token = TOKENS[i % len(TOKENS)]
        print(f"\nSpieler {i+1}, gib deinen Namen ein:")
        name = input(f"({token}) >> ")
        if name == "": name = f"Spieler {i+1}"
        spieler_liste.append(Spieler(name, token))
    
    # 2. GAME LOOP
    running = True
    runde = 1
    
    while running:
        for spieler in spieler_liste:
            clear()
            print(f"{F.BG_BLUE}{F.WHITE} RUNDE {runde} {F.RESET} | {spieler.token} {F.BOLD}{spieler.name}{F.RESET} ist dran!")
            linie()
            
            # Status Board anzeigen
            print(f"Position: {BOARD[spieler.pos]['name']}")
            print("Drücke [ENTER] zum Würfeln...")
            input()
            
            wurf = animierter_wuerfel()
            
            # Bewegung animieren (Text)
            print("Du läufst los...")
            alter_pos = spieler.pos
            for _ in range(wurf):
                time.sleep(0.3)
                spieler.pos = (spieler.pos + 1) % len(BOARD)
                # Kleines visuelles Feedback beim Laufen
                sys.stdout.write(f" -> {BOARD[spieler.pos]['name'][:3]}")
                sys.stdout.flush()
            print("\n")
            
            # Über LOS Check
            if spieler.pos < alter_pos:
                print(f"{F.GREEN} $$$ ÜBER LOS! $$$ {F.RESET} Verteile 2 Schlücke!")
                time.sleep(1)

            aktuelles_feld = BOARD[spieler.pos]
            
            # VISUALISIERUNG DER KARTE
            draw_card(aktuelles_feld, spieler)
            time.sleep(0.5)
            
            # LOGIK
            typ = aktuelles_feld["typ"]
            
            if typ == "str" or typ == "bahn":
                besitzer = None
                # Check ob gekauft (einfache Logik)
                for s in spieler_liste:
                    if spieler.pos in s.besitz:
                        besitzer = s
                
                if besitzer is None:
                    print(f"Zu kaufen für {aktuelles_feld['preis']} Schlücke?")
                    entscheidung = input("[j] Kaufen (trinken) | [n] Weiter >> ")
                    if entscheidung.lower() == "j":
                        print(f"{F.GREEN}Gekauft!{F.RESET} Das gehört jetzt dir.")
                        spieler.besitz.append(spieler.pos)
                    else:
                        print("Du ziehst weiter.")
                elif besitzer == spieler:
                    print(f"{F.GREEN}Willkommen zuhause!{F.RESET}")
                else:
                    miete = aktuelles_feld['preis']
                    print(f"{F.RED}STOPP!{F.RESET} Das gehört {besitzer.name}.")
                    print(f"Zahle {miete} Schlücke Miete!")
            
            elif typ == "event" or typ == "jail":
                aufgabe = random.choice(kartenstapel)
                print(f"{F.YELLOW}AUFGABE:{F.RESET}")
                typewriter(aufgabe, 0.05)
            
            print("\n" + "-"*30)
            input("Drücke Enter für den nächsten Spieler...")
        
        runde += 1

if __name__ == "__main__":
    spiel_starten()

import random
import time
import os

# --- AUFGABEN-POOLS ---

# Basis-Aufgaben (für alle Modi)
TASKS_COMMON = [
    "Alle trinken einen Schluck auf die Freundschaft.",
    "Kategorie-Spiel: Automarken. Der erste, dem nichts einfällt, trinkt 2.",
    "Reim-Runde: Ein Wort reimen. Wer es nicht schafft, trinkt.",
    "Der Spieler links von dir darf eine Regel erfinden.",
    "Alle, die ein 'e' im Namen haben, trinken."
]

# Modus 16+: Fokus auf Trinken & Party
TASKS_16 = [
    "Wasserfall! Alle trinken, bis du absetzt.",
    "Verteile 4 Schlücke an jemanden, der noch nüchtern aussieht.",
    "Schere-Stein-Papier gegen den Bankhalter. Verlierer trinkt 3.",
    "Medusa: Alle schauen nach unten. Auf 3 hochschauen. Wer Blickkontakt hat, trinkt.",
    "Fragerunde: Du bist der 'Question Master'. Wer deine Fragen beantwortet, trinkt."
]

# Modus 18+: Fokus auf Wahrheit, Pflicht & Intimeres (Hot Seat)
TASKS_18 = [
    "Wahrheit oder Drink: Erzähle deinen peinlichsten Kuss-Moment oder trinke 4.",
    "Körperkontakt: Umarme den Spieler rechts von dir für 10 Sekunden (oder beide trinken 3).",
    "Handy-Check: Lies die letzte WhatsApp-Nachricht vor oder trinke 5.",
    "Strip-Poker Light: Lege ein Kleidungsstück ab (Socken zählen!) oder trinke den Rest deines Glases.",
    "Hot Seat: Die Gruppe darf dir eine intime Frage stellen. Antworte ehrlich oder trinke 5.",
    "Kuss-Roulette: Wirf eine Münze. Kopf = Kuss auf die Wange bei links, Zahl = bei rechts. Verweigern = 5 Schlücke.",
    "Bewerte die Fahrkünste deiner Mitspieler. Der Schlechteste trinkt 3 aus Frust."
]

# SPIELFELD-STRUKTUR (Kompakt)
SPIELFELD = [
    {"name": "LOS", "typ": "start"},
    {"name": "Kneipenstraße", "typ": "feld", "preis": 2},
    {"name": "EREIGNIS", "typ": "karte"},
    {"name": "Bier-Allee", "typ": "feld", "preis": 3},
    {"name": "POLIZEIKONTROLLE", "typ": "strafe", "aktion": "Pusten! Wenn du lallst, trinke 3."},
    {"name": "Bahnhof Nord", "typ": "feld", "preis": 4},
    {"name": "Schnapsgasse", "typ": "feld", "preis": 4},
    {"name": "EREIGNIS", "typ": "karte"},
    {"name": "Clubmeile", "typ": "feld", "preis": 5},
    {"name": "AUSNÜCHTERUNGSZELLE", "typ": "pause", "aktion": "Besuch: Alles gut. Pause."},
    {"name": "Weinberg", "typ": "feld", "preis": 5},
    {"name": "EREIGNIS", "typ": "karte"},
    {"name": "Wodka-Platz", "typ": "feld", "preis": 6},
    {"name": "Blackout-Boulevard", "typ": "feld", "preis": 8},
]

class Spieler:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.besitz = []

def clear_screen():
    # Löscht den Bildschirm für bessere Übersicht (funktioniert in den meisten Terminals)
    os.system('cls' if os.name == 'nt' else 'clear')

def spiel_starten():
    clear_screen()
    print("🍾 WILLKOMMEN BEIM GITHUB-TRINK-MONOPOLY 🍾")
    print("---------------------------------------------")
    
    # Modus-Auswahl
    while True:
        try:
            modus = int(input("Wähle den Modus:\n[1] 16+ (Party & Trinken)\n[2] 18+ (Wahrheit, Pflicht & Spicy)\n>> Deine Wahl: "))
            if modus in [1, 2]:
                break
        except ValueError:
            pass
            
    aktiver_kartenstapel = TASKS_COMMON + (TASKS_16 if modus == 1 else TASKS_18)
    modus_name = "PARTY (16+)" if modus == 1 else "HARDCORE (18+)"
    
    print(f"\nModus gewählt: {modus_name}")
    anzahl = int(input("Anzahl der Spieler: "))
    spieler_liste = [Spieler(input(f"Name Spieler {i+1}: ")) for i in range(anzahl)]
    
    runde = 1
    running = True
    
    while running:
        print(f"\n--- RUNDE {runde} ({modus_name}) ---")
        for spieler in spieler_liste:
            input(f"\n>> {spieler.name} würfelt... [ENTER]")
            
            wurf = random.randint(1, 6)
            print(f"🎲 Wurf: {wurf}")
            
            spieler.position = (spieler.position + wurf) % len(SPIELFELD)
            feld = SPIELFELD[spieler.position]
            
            print(f"📍 Feld: {feld['name']}")
            
            if feld["typ"] == "feld":
                # Vereinfachte Kauf-Logik für schnelleren Spielfluss
                if any(spieler.position in s.besitz for s in spieler_liste):
                    besitzer = next(s for s in spieler_liste if spieler.position in s.besitz)
                    if besitzer != spieler:
                        print(f"💸 Gehört {besitzer.name}. Trinke {feld['preis']} Schlücke Miete!")
                    else:
                        print("🏠 Dein Haus. Alles entspannt.")
                else:
                    print(f"Kaufen für {feld['preis']} Schlücke? (j/n)")
                    if input(">> ").lower() == "j":
                        spieler.besitz.append(spieler.position)
                        print("✅ Gekauft! Du hast getrunken.")
            
            elif feld["typ"] == "karte":
                karte = random.choice(aktiver_kartenstapel)
                print(f"🃏 AUFGABE: {karte}")
            
            elif "aktion" in feld:
                print(f"⚡ {feld['aktion']}")
                
        if input("\nNächste Runde? (q zum Beenden, Enter weiter): ").lower() == "q":
            running = False
        runde += 1

if __name__ == "__main__":
    spiel_starten()

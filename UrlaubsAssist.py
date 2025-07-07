import json
import os
import time

DATEI = "urlaube.json"

STANDARD_URLAUBSTAGE = 30

def initialisiere_datei():
    if not os.path.exists(DATEI):
        speichere_daten({"mitarbeiter": {}, "antraege": []})

def lade_daten():
    with open(DATEI, "r", encoding="utf-8") as f:
        return json.load(f)

def speichere_daten(daten):
    with open(DATEI, "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=2)

def mitarbeiter_hinzufuegen():
    name = input("Name des Mitarbeiters: ").strip()
    if not name:
        print("Ungültiger Name.")
        return

    daten = lade_daten()
    if name in daten["mitarbeiter"]:
        print("Mitarbeiter existiert bereits.")
        return

    daten["mitarbeiter"][name] = {"urlaubstage": STANDARD_URLAUBSTAGE}
    speichere_daten(daten)
    print(f"{name} wurde mit {STANDARD_URLAUBSTAGE} Urlaubstagen hinzugefügt.")

def urlaub_beantragen():
    name = input("Name des Mitarbeiters: ").strip()
    try:
        tage = int(input("Anzahl der Urlaubstage: ").strip())
        if tage <= 0:
            raise ValueError
    except ValueError:
        print("Bitte eine gültige positive Zahl eingeben.")
        return

    daten = lade_daten()
    if name not in daten["mitarbeiter"]:
        print("Mitarbeiter nicht gefunden.")
        return

    daten["antraege"].append({"name": name, "tage": tage, "status": "offen"})
    speichere_daten(daten)
    print(f"Urlaubsantrag für {name} gespeichert.")

def antraege_anzeigen():
    daten = lade_daten()
    antraege = daten.get("antraege", [])

    if not antraege:
        print("Keine Anträge vorhanden.")
        return

    for i, antrag in enumerate(antraege):
        print(f"{i}: {antrag['name']} - {antrag['tage']} Tage ({antrag['status']})")

def antrag_bearbeiten():
    daten = lade_daten()
    antraege = daten["antraege"]

    if not antraege:
        print("Keine Anträge zu bearbeiten.")
        return

    antraege_anzeigen()
    try:
        index = int(input("Antragsnummer zur Bearbeitung: ").strip())
        if not (0 <= index < len(antraege)):
            raise IndexError
    except (ValueError, IndexError):
        print("Ungültige Eingabe.")
        return

    antrag = antraege[index]
    entscheidung = input("Genehmigen (g) oder Ablehnen (a)? ").strip().lower()

    if entscheidung == "g":
        name = antrag["name"]
        tage = antrag["tage"]
        resttage = daten["mitarbeiter"][name]["urlaubstage"]

        if resttage >= tage:
            daten["mitarbeiter"][name]["urlaubstage"] -= tage
            antrag["status"] = "genehmigt"
            print("Antrag genehmigt.")
        else:
            print(f"Nicht genügend Urlaubstage (verfügbar: {resttage}).")
    elif entscheidung == "a":
        antrag["status"] = "abgelehnt"
        print("Antrag abgelehnt.")
    else:
        print("Ungültige Eingabe.")

    speichere_daten(daten)

def menue():
    aktionen = {
        "1": mitarbeiter_hinzufuegen,
        "2": urlaub_beantragen,
        "3": antraege_anzeigen,
        "4": antrag_bearbeiten
    }

    while True:
        print("\n[1] Mitarbeiter hinzufügen\n[2] Urlaubsantrag stellen\n[3] Anträge anzeigen\n[4] Antrag bearbeiten\n[5] Beenden")
        wahl = input("Wählen Sie eine Option (1-5): ").strip()

        if wahl == "5":
            print("Programm beendet.")
            break
        aktion = aktionen.get(wahl)
        if aktion:
            aktion()
        else:
            print("Ungültige Eingabe.")
        time.sleep(1)

if __name__ == "__main__":
    initialisiere_datei()
    menue()
import json
import os
import time

DATEI = "urlaube.json"

if not os.path.exists(DATEI):
    with open(DATEI, "w") as f:
        json.dump({"mitarbeiter": {}, "antraege": []}, f)

def lade_daten():
    with open(DATEI, "r") as f:
        return json.load(f)

def speichere_daten(daten):
    with open(DATEI, "w") as f:
        json.dump(daten, f, indent=2)

def mitarbeiter_hinzufuegen():
    name = input("Geben Sie den Namen des Mitarbeiters ein: ").strip()
    daten = lade_daten()
    if name not in daten["mitarbeiter"]:
        daten["mitarbeiter"][name] = {"urlaubstage": 30}  # Standardurlaubstage
        speichere_daten(daten)
        print(f"{name} wurde hinzugefügt.")
    else:
        print("Mitarbeiter existiert bereits.")

def urlaub_beantragen():
    name = input("Geben Sie den Namen des Mitarbeiters ein: ").strip()
    tage = int(input("Wie viele Tage Urlaub möchten Sie beantragen? "))
    daten = lade_daten()
    if name in daten["mitarbeiter"]:
        antrag = {"name": name, "tage": tage, "status": "offen"}
        daten["antraege"].append(antrag)
        speichere_daten(daten)
        print(f"Urlaubsantrag für {name} mit {tage} Tagen gespeichert.")
    else:
        print("Mitarbeiter nicht gefunden.")

def antraege_anzeigen():
    daten = lade_daten()
    if not daten["antraege"]:
        print("Keine Anträge vorhanden.")
    for i, antrag in enumerate(daten["antraege"]):
        print(f"{i}: {antrag['name']} will {antrag['tage']} Tage Urlaub ({antrag['status']})")

def antrag_bearbeiten():
    daten = lade_daten()
    if not daten["antraege"]:
        print("Keine Anträge zu bearbeiten.")
        return
    antraege_anzeigen()  # Zeigt die vorhandenen Anträge an
    index = int(input("Geben Sie die Nummer des Antrags ein, den Sie bearbeiten möchten: "))
    if index < 0 or index >= len(daten["antraege"]):
        print("Ungültige Auswahl.")
        return
    antrag = daten["antraege"][index]
    entscheidung = input("Möchten Sie den Antrag genehmigen (g) oder ablehnen (a)? ").strip().lower()
    if entscheidung == "g":
        name = antrag["name"]
        tage = antrag["tage"]
        if daten["mitarbeiter"][name]["urlaubstage"] >= tage:
            daten["mitarbeiter"][name]["urlaubstage"] -= tage
            antrag["status"] = "genehmigt"
            print("Antrag genehmigt.")
        else:
            print("Nicht genügend Urlaubstage.")
    elif entscheidung == "a":
        antrag["status"] = "abgelehnt"
        print("Antrag abgelehnt.")
    else:
        print("Ungültige Eingabe.")
    speichere_daten(daten)

def menue():
    while True:
        print("\n[1] Mitarbeiter hinzufügen\n[2] Urlaubsantrag stellen\n[3] Anträge anzeigen\n[4] Antrag bearbeiten\n[5] Beenden")
        wahl = input("Wählen Sie eine Option (1-5): ").strip()
        if wahl == "1":
            mitarbeiter_hinzufuegen()
        elif wahl == "2":
            urlaub_beantragen()
        elif wahl == "3":
            antraege_anzeigen()
        elif wahl == "4":
            antrag_bearbeiten()
        elif wahl == "5":
            print("Programm beendet.")
            break
        else:
            print("Ungültige Eingabe. Bitte wählen Sie eine Zahl zwischen 1 und 5.")
        time.sleep(1)

if __name__ == "__main__":
    menue()
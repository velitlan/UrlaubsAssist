import json
import os
import time
import csv

DATEI = "urlaube.json"
STANDARD_URLAUBSTAGE = 30

def initialisiere_datei():
    if not os.path.exists(DATEI) or os.stat(DATEI).st_size == 0:
        speichere_daten({"mitarbeiter": {}, "antraege": []})

def lade_daten():
    try:
        with open(DATEI, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Fehler beim Laden der Datei. Daten werden neu initialisiert.")
        speichere_daten({"mitarbeiter": {}, "antraege": []})
        return {"mitarbeiter": {}, "antraege": []}

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

    eingabe = input(f"Urlaubstage für {name} (Enter für Standard = {STANDARD_URLAUBSTAGE}): ").strip()
    if eingabe == "":
        tage = STANDARD_URLAUBSTAGE
    else:
        try:
            tage = int(eingabe)
            if tage <= 0:
                raise ValueError
        except ValueError:
            print("Ungültige Zahl für Urlaubstage.")
            return

    daten["mitarbeiter"][name] = {"urlaubstage": tage}
    speichere_daten(daten)
    print(f"{name} wurde mit {tage} Urlaubstagen hinzugefügt.")

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

def exportiere_csv_daten():
    daten = lade_daten()

    with open("mitarbeiter.csv", "w", newline='', encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Name", "Verbleibende Urlaubstage"])
        for name, info in daten["mitarbeiter"].items():
            writer.writerow([name, info["urlaubstage"]])

    with open("antraege.csv", "w", newline='', encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Name", "Tage", "Status"])
        for antrag in daten["antraege"]:
            writer.writerow([antrag["name"], antrag["tage"], antrag["status"]])

    print("CSV-Daten wurden erfolgreich exportiert.")

def menue():
    while True:
        print("\n[1] Mitarbeiter hinzufügen\n[2] Urlaubsantrag stellen\n[3] Anträge anzeigen\n[4] Antrag bearbeiten\n[5] CSV exportieren\n[6] Beenden")
        wahl = input("Wählen Sie eine Option (1-6): ").strip()
        if wahl == "1":
            mitarbeiter_hinzufuegen()
        elif wahl == "2":
            urlaub_beantragen()
        elif wahl == "3":
            antraege_anzeigen()
        elif wahl == "4":
            antrag_bearbeiten()
        elif wahl == "5":
            exportiere_csv_daten()
        elif wahl == "6":
            exportiere_csv_daten()
            print("Programm beendet.")
            break
        else:
            print("Ungültige Eingabe.")
        time.sleep(1)

if __name__ == "__main__":
    initialisiere_datei()
    menue()
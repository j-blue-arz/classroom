# Sitzplan-Generator

Ein Programmierprojekt für Schülerinnen und Schüler der Mittelstufe.

## Worum geht es?

Der Sitzplan-Generator hilft Lehrkräften dabei, einen Sitzplan für ihr Klassenzimmer zu erstellen. Die Anwendung verteilt Schülerinnen und Schüler automatisch auf die vorhandenen Tische und berücksichtigt dabei Regeln, zum Beispiel dass niemand isoliert sitzen soll.

Das Projekt ist als Startercode für ein Praktikum gedacht: Die Grundstruktur steht bereits, und durch verschiedene Aufgaben wird die Anwendung Schritt für Schritt erweitert und verbessert.

## Inhalt

Die Anwendung besteht aus folgenden Dateien:

- `main.py`: Einstiegspunkt, definiert Model und Controller
- `gui.py`: grafische Oberfläche (tkinter)
- `classroom.py`: Datenmodell für den Grundriss des Klassenzimmers
- `students.py`: Liste der Schülerinnen und Schüler
- `constraints.py`: Regeln für die Sitzplatzvergabe und Algorithmus

Die Anwendung folgt dem **MVC-Muster** (Model–View–Controller): Daten, Logik und Oberfläche sind klar voneinander getrennt. Das Projekt ist bewusst einfach gehalten, um für die Mittelstufe angemessen zu sein.

## Erweiterungen

Mit beigelegten Aufgaben wird die Anwendung schrittweise erweitert:

- **Darstellung anpassen** - Fenster einzeichnen, Farben und Größen verändern, den Grundriss an das eigene Klassenzimmer anpassen
- **Neue Regeln hinzufügen** - eigene Constraints schreiben, z.B. wer neben wem sitzen soll oder muss
- **Funktionalität erweitern** - Schülerinnen und Schüler über die Oberfläche hinzufügen, Tische per Mausklick bearbeiten, und mehr
- **Daten speichern und laden** - Grundriss und Schülerliste in einer Datei ablegen, damit Änderungen beim nächsten Start erhalten bleiben

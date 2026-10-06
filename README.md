# DienstplanConverter 1.0

Kleines vollständig lokales Windows-Programm: Es liest den Monatsdienstplan für
**Klein** aus einer `.xlsx` und erzeugt eine gut lesbare, einseitige PDF im
**A4-Querformat**. Zwei Tabellen teilen den Monat gleichmäßig; beide Dienstzeilen
und leere Zellen bleiben erhalten. Excel-Farben werden nicht übernommen.

## Projektstruktur

- `src/dienstplan_converter/`: Datenmodell, Parser, Renderer, Theme und Dialoge
- `tests/`: Unit- und Regressionstests, unveränderte echte Dateien in `fixtures/`
- `docs/ANALYSE.md`: Fixture-Analyse und Implementierungsplan
- `docs/desired_layout.png`: Layoutreferenz
- `docs/examples/`: aus echten Fixtures erzeugte Beispiel-PDFs
- `build.ps1`, `windows_entry.py`: Windows-EXE-Build

## Entwicklung und Tests

Python **3.11 oder neuer**, empfohlen **3.12** mit Tkinter. Unter Windows enthält
die normale python.org-Installation Tkinter. Unter Debian/Ubuntu gegebenenfalls
`python3-venv` und `python3-tk` installieren. Parser und PDF-Tests funktionieren
auch ohne grafische Umgebung und ohne Tkinter.

Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pytest -q
.venv/bin/python -m dienstplan_converter
.venv/bin/python -m dienstplan_converter tests/fixtures/dienstplan_2026_04.xlsx
```

Windows (PowerShell):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m dienstplan_converter
.\.venv\Scripts\python.exe -m dienstplan_converter "C:\Dienstplaene\April.xlsx"
```

Alternativ stehen alle Laufzeit- und Entwicklungsabhängigkeiten in
`requirements.txt`. Installation benötigt Internet oder ein lokales Paketarchiv;
die fertige Anwendung benötigt keinerlei Internetzugriff.

Ohne Argument öffnet sich ein Dateidialog; Abbrechen beendet die Anwendung ruhig.
Mit genau einem Dateipfad wird dieser direkt verarbeitet. Ein Dialog zeigt Erfolg
oder einen verständlichen Fehler. Der interaktive Start benötigt eine grafische
Umgebung. Rein programmatisch unter Linux ohne GUI:

```python
from pathlib import Path
from dienstplan_converter.main import convertFile

pdfPath = convertFile(Path("tests/fixtures/dienstplan_2026_04.xlsx"))
print(pdfPath)
```

## Windows-EXE bauen

**Den finalen Build unter Windows ausführen.** PyInstaller auf Linux erzeugt keine
Windows-EXE. Benötigt werden Python 3.12 einschließlich Tkinter und PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\build.ps1
```

Das Skript richtet bei Bedarf `.venv` ein, installiert die Abhängigkeiten, führt
alle Tests aus und baut mit `--onefile --windowed`:

```text
dist/DienstplanConverter.exe
```

Die EXE benötigt beim Endbenutzer weder Python noch Excel, LibreOffice, Browser,
Server oder Datenbank. Tk und die Python-Bibliotheken werden durch PyInstaller
mitgenommen. Auf einem Windows-Rechner ohne Python abschließend prüfen: Datei auf
die EXE ziehen, Doppelklick/Dateiauswahl, Abbrechen und geöffnete/gesperrte Ziel-PDF.
Der Windows-Build und echte Windows-Dialoge wurden in der Linux-VM nicht ausgeführt.

## Verwendung

Eine `.xlsx` auf `DienstplanConverter.exe` ziehen. Alternativ die EXE doppelklicken
und eine Datei auswählen. Die Erfolgsmeldung nennt den Speicherort; danach endet
das Programm. Es erzeugt neben der Quelldatei beispielsweise:

```text
C:\Dienstplaene\Dienstplan_Klein_April_2026.pdf
```

Schema: `Dienstplan_Klein_<DeutscherMonatsname>_<Jahr>.pdf`. Eine vorhandene PDF wird
ersetzt. Ist sie gesperrt oder fehlt die Schreibberechtigung, erscheint eine
Fehlermeldung. Die PDF wird vor dem Ersetzen vollständig in eine temporäre Datei
im Zielordner geschrieben. Die Excel-Datei wird ausschließlich lesend geöffnet.

Unerwartete Fehler werden lokal in
`%LOCALAPPDATA%\DienstplanConverter\DienstplanConverter.log` protokolliert
(unter Linux im Home-Verzeichnis; bei Schreibfehlern im aktuellen Verzeichnis).
Es gibt keine Telemetrie oder Netzwerkübertragung.

## Layout und Erkennung

Layoutwerte stehen zentral in `theme.py`: Ränder, Schriftgrößen, Farben,
Linienstärken, Zeilenhöhen, Tabellenabstand und Padding. Wochenenden sind grau
hinterlegt und über die fett gedruckten Kürzel **Sa/So** auch ohne Farbe erkennbar.
Lange Dienstwerte erhalten eine kleinere Schrift, damit ihr Inhalt vollständig
in die Tageszelle passt.

Die Erkennung liest höchstens die ersten **30 Zeilen × 80 Spalten** pro Blatt;
Monatsangaben werden in den ersten zehn Zeilen gesucht. Anker sind Monatsname und
Jahr, `Mitarbeiter/Tag`, die vollständige Tagesfolge und `Klein`. Das Programm
berechnet Tagesanzahl und Wochentage selbst. Zusätzliche Daten rechts und Tage des
Folgemonats werden ignoriert. Oktober `7 (2x)` und vertikale Versätze werden
unterstützt. Bei mehreren erkennbaren Monatsplänen wird zur Vermeidung einer
versehentlichen Auswahl abgebrochen. Neue Quellsysteme außerhalb dieser Grenzen
können eine Anpassung des Parsers benötigen. Formeln werden als zuletzt von Excel
gespeicherte Werte gelesen; die Anwendung berechnet keine Excel-Formeln.

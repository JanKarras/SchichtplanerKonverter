# V1 – Verifikation und Selbstreview

Entwicklung unter Linux mit Python 3.12. Finaler Lauf:

```text
.venv/bin/python -m pytest -q
45 passed in 0.67s
```

Geprüft:
- Alle fünf realen Fixtures: Monat, Jahr, Mitarbeiter, Tagesanzahl und stabile Dienstwerte.
- Beide Zeilen, Leerstellen, horizontale/vertikale Verschiebung, Oktober-Anmerkung.
- Januar/Folgemonat explizit sowie Zusatzdaten rechts, Februar normal und Schaltjahr.
- Bounded-read-Test prüft die exakten 30 × 80 Leseparameter; echte Fixtures werden schnell verarbeitet.
- Ungültige Dateien, fehlende Anker, falsche Tagesfolge und mehrdeutige Arbeitsmappen.
- Monatsteilung für 28/29/30/31 Tage und deutsche Ausgabedateinamen.
- PDF-Seitenanzahl und A4-Querformat für alle vier Monatslängen mit pypdf.
- End-to-End-Konvertierung, Überschreiben, Quellschutz, Schreibfehler und simulierte Dateisperre.
- Dateiauswahl/Abbrechen, Argumente, Fehlermeldungen, Log und Root-Cleanup mit Dialog-Mocks.

April und Oktober wurden aus den echten Fixtures als Beispiel-PDFs erzeugt.
Die gerenderte Oktoberseite wurde visuell geprüft: zwei breite Tabellen, getrennte
Dienstzeilen, Wochenende ohne Farbabängigkeit erkennbar, lange Zeitangabe vollständig,
31 Tage auf einer Seite. Die zweite Tabelle nutzt ihre eigene Tagesbreite.

Selbstreview: kein Iterieren bis max_row, read-only Workbook mit finally-close,
keine Änderungen an Quelldateien, Kalenderwerte aus Standardbibliothek, PDF-Kern
unabhängig von Excel-Zellen und Tk. Speichern erfolgt über eine temporäre Datei
im Zielordner und anschließendes Ersetzen, damit ein fehlgeschlagener Schreibvorgang
keine bestehende PDF frühzeitig leert. Fehler werden verständlich angezeigt;
unerwartete Details bleiben im lokalen Log. AST-Prüfung: maximal vier Funktionen
je Quelldatei und camelCase-Funktionsnamen.

SHA-256 aller fünf Fixtures vor/nach der Implementierung identisch.

Offene Plattformprüfung: Windows-EXE muss unter Windows mit build.ps1 gebaut und
auf einem Windows-System ohne Python getestet werden. Linux kann diesen Build
nicht verifizieren. Echte Dateisperren und native Dialoge wurden hier durch Tests
simuliert. Diese VM hat kein Tkinter; Parser, PDF und Tests funktionieren dennoch.

## Finaler Pre-Windows-QA-Review

Erneut geprüft: gesamte Implementierung, sys.argv und Einstiegspunkt,
Dateidialog/Abbruch, Erfolg/Fehler und Root-Cleanup, Pfade mit Leerzeichen und
Umlauten sowie Großschreibung `.XLSX`, bestehende PDF, Dateisperre und realer
POSIX-schreibgeschützter Zielordner. Keine Linux-spezifischen Pfadannahmen im
Anwendungscode. build.ps1 ist für Python 3.12 unter Windows plausibel;
`--onefile --windowed`, Paketpfad und Fehlercodes sind korrekt gesetzt.

Konkrete Korrekturen: Temp-Datei-Cleanup kann keinen verständlichen Speicherfehler
mehr verdecken; Tk-Cleanup lässt keine Exception nach dem Dialog entweichen.
Beide Cleanup-Fehler werden lokal protokolliert. Der Build prüft Tkinter vorab,
da die Dialog-Mocks eine Python-Installation ohne Tkinter nicht erkennen würden.
Keine neue Funktionalität und keine Layoutänderungen.

April und Oktober erneut rasterisiert und visuell mit der Referenz verglichen:
Titel und beide Tabellen vollständig, keine abgeschnittenen Texte/Überlappungen.
Programmatisch je genau eine A4-Querformatseite, alle Tagesnummern und Inhalte
beider Dienstzeilen geprüft. Alle Fixture-Hashes weiterhin unverändert.

Finaler Testlauf: **52 bestanden**. Der POSIX-Test für Ordner-Schreibrechte wird
unter Windows übersprungen; dort müssen echte Windows-ACLs geprüft werden.
Noch ausschließlich unter Windows: PowerShell/PyInstaller-Build, EXE auf einem
System ohne Python, Explorer-Drag-and-Drop, echte Tk-Dialoge, Windows-ACLs und
Dateisperren sowie Pfade mit Umlauten/Leerzeichen durch Explorer und die EXE.

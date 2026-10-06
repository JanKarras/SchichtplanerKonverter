# Analyse und Implementierungsplan

Das Repository enthielt ausschließlich fünf echte XLSX-Fixtures und das Layoutbild.
Es gibt keine zusätzliche AGENTS.md. Die global übergebenen Regeln gelten;
ECC python-patterns unterstützt Typisierung, Ressourcenverwaltung und Modulgrenzen.

| Monat 2026 | Tageszeile | Header | Klein-Zeilen | Tage |
|---|---|---|---|---|
| Januar | 3 | 4 | 7–8 | 31 |
| April | 3 | 4 | 7–8 | 30 |
| August | 3 | 4 | 7–8 | 31 |
| September | 3 | 4 | 7–8 | 30 |
| Oktober | 4 | 5 | 8–9 | 31 |

Monatsangaben enthalten teils doppelte Leerzeichen. Tageswerte sind Zahlen oder
Strings wie `01`; Oktober enthält `7 (2x)`. Januar hat rechts den 1. Februar,
April zusätzliche Werte (z.B. AK8). Maximaldimensionen reichen bis Zeile 1048517.
Die Daten liegen dennoch vollständig im oberen Bereich. Suchfenster: 30 × 80.
Die obere Zusatzzeile enthält Hinweise/Zeiten und wird gemäß Spezifikation nicht
übernommen. Die beiden Klein-Zeilen bleiben getrennt, Leerstellen positionsgetreu.

Das Referenzbild zeigt zwei breite Tabellen mit Tages- und Wochentagskopf und
zusammengeführter Mitarbeiterbeschriftung. Die V1 übernimmt diese Struktur mit
eigenem druckerfreundlichem Design, ohne Excel-Farben oder Zusatzkopfzeile.

Plan in Reihenfolge:
1. Unveränderliches Datenmodell und begrenzter read-only Parser mit Ankern.
2. Regressionen für sämtliche Fixtures, Leerstellen, Versatz und Folgemonat.
3. Zentraler Theme und einseitiger A4-Querformat-Renderer mit dynamischer Teilung.
4. Dateipfadargument, nativer Dateidialog, Meldungen und lokales Fehlerlog.
5. Windows-PyInstaller-Build, README, Selbstreview, PDF-Prüfung und Fixture-Hashes.

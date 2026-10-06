# Excel-Farben im freigegebenen PDF-Layout

Alle fünf echten Fixtures wurden im eigentlichen Monatsbereich untersucht:
Tagesnummer, Wochentag und die zwei Klein-Zeilen. Hinweise/Zeitangaben oberhalb
und Zusatzbereiche rechts werden nicht auf das PDF übertragen.

Alle relevanten Füllungen sind `solid`, gespeichert als ARGB oder Theme mit Tint.
Indexed/Auto, Muster, Verläufe und bedingte Formatierungen kommen dort nicht vor;
auch die Worksheet-XMLs enthalten keine bedingten Formatierungen.

| Monat | RGB-Hervorhebungen | Theme-Füllungen |
|---|---|---|
| Januar | Rosa `FF7C80`, Gold `FFC000` | Weiß, abgedunkeltes Weiß/Grau, helles Blau |
| April | Violett `CC66FF`, Grün `92D050`, Orange `FFA589`, Blau `00B0F0` | Weiß/Grau |
| August | Grün `92D050`, Gelb `FFFF00` | Weiß/Grau, helles Blau, helles Grün |
| September | Violett `CC66FF`, Grün `92D050`, Rosa `FFCCFF` | Weiß/Grau, helles Blau |
| Oktober | Violett `CC66FF`, Grün `92D050`, Rot `FF0000`, Gelb `FFFF00`, Rosa `FFCCFF`, Gold `FFC000` | Weiß/Grau |

Theme 0 ist das aus der Arbeitsmappe gelesene Weiß, mit Tint etwa -0,15 ergibt es
`#D9D9D9`. Theme 4 mit Tint etwa +0,80 ergibt helles Blau `#DEEBF7`; Theme 9 mit
entsprechendem Tint helles Grün `#E2F0D9`. Die Theme-Palette wird je Arbeitsmappe
gelesen, nicht als feste Office-Farbpalette angenommen. Tint wird über HLS-Luminanz
berechnet; die RGB-Ausgabe wird am Ende auf 8 Bit gerundet.

Eine Tages-Spalte ist nicht generell einfarbig. Tages- und Wochentagskopf sind
häufig anders gefärbt als der Dienstbereich. Die beiden Dienstzeilen stimmen in
vier Fixtures vollständig überein. Oktober weicht an Tag 11, 19 und 20 zwischen
den beiden Zeilen ab. Daher speichert DayEntry separat `headerColor`,
`weekdayColor`, `primaryColor`, `secondaryColor` als `#RRGGBB` oder `None`.
Auch farbig gefüllte leere Zellen werden positionsgetreu übernommen.

Der Parser bleibt read-only und liest weiterhin ausschließlich 30 × 80 Zellen;
die semantische Erkennung und Begrenzung auf die echten Kalendertage bleiben
unverändert. Der Renderer erhält nur Modellwerte. Explizite Excel-Farbe inklusive
Weiß hat pro Zelle Vorrang, danach folgt neutrale Wochenendfüllung, sonst Weiß.
Textfarbe Schwarz/Weiß wird nach dem größeren WCAG-Kontrast aus linearer
RGB-Luminanz gewählt. Das freigegebene Layout einschließlich Größen, Abständen,
Schriftanpassung und Seitenformat bleibt unverändert.

Grenzen: Systemfarben/Auto und reservierte Indexed-Farben 64/65 besitzen keinen
portablen eindeutigen RGB-Wert; ebenso lassen sich Muster/Verläufe nicht als eine
Füllfarbe wiedergeben. Fehlende/unauflösbare Farben erhalten die neutrale
Darstellung. Bedingte Formatierungen werden nicht ausgewertet. Diese Fälle treten
in den Fixtures nicht auf.

Verifikation: 84 Tests bestanden. Neue Tests prüfen RGB, Theme-Reihenfolge,
Arbeitsmappenpalette, Tint, Indexed inklusive eigener Palette, Fallbacks,
Leerzellen, Versatz, Folgemonat/Zusatzbereiche, getrennte Zeilenfarben und Kontrast.
Alle fünf Beispiel-PDFs neu erzeugt, als eine A4-Querformatseite geprüft und
visuell kontrolliert: korrekte Zellenfarben, guter Kontrast, keine Verschiebungen,
Überlappungen oder abgeschnittenen Inhalte. Alle Fixture-Hashes unverändert.

Referenzen:
- [openpyxl: Farben und Zellstile](https://openpyxl.readthedocs.io/en/3.1/styles.html)
- [Microsoft: OOXML-Farben und Tint](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.spreadsheet.foregroundcolor?view=openxml-3.0.1)

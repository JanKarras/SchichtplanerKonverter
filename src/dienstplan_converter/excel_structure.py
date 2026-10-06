"""Semantische Erkennung innerhalb eines bereits begrenzten Zellfensters."""
import calendar
import re
from typing import Any

from .calendar_utils import MONTH_NAMES
from .errors import ConversionError

SEARCH_ROWS = 30
SEARCH_COLUMNS = 80


def findMonth(rows: tuple[tuple[Any, ...], ...]) -> tuple[int, int]:
    monthPattern = '|'.join(MONTH_NAMES[1:])
    foundMonth = False
    matches = set()
    for row in rows[:10]:
        for value in row:
            text = str(value or '')
            if re.search(rf'\b({monthPattern})\b', text, re.I):
                foundMonth = True
            match = re.search(rf'\b({monthPattern})\s+(\d{{4}})\b', text, re.I)
            if match:
                month = next(i for i, name in enumerate(MONTH_NAMES) if name.casefold() == match[1].casefold())
                year = int(match[2])
                if 1900 <= year <= 9999:
                    matches.add((month, year))
    if len(matches) != 1:
        message = 'Monat und Jahr konnten nicht eindeutig erkannt werden.'
        if not matches:
            message = 'Das Jahr konnte nicht gefunden werden.' if foundMonth else 'Der Monat konnte nicht gefunden werden.'
        raise ConversionError(message)
    return matches.pop()


def dayNumber(value: Any) -> int | None:
    # Allow the real October annotation, but never accept fractional numbers.
    match = re.fullmatch(r'\s*(\d{1,2})(?:\s*\(2x\))?\s*', str(value), re.I)
    if match:
        return int(match[1])
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return None


def findStructure(rows: tuple[tuple[Any, ...], ...], month: int, year: int) -> tuple[int, int, int, int, int]:
    headers = [(r, c) for r, row in enumerate(rows) for c, value in enumerate(row)
               if re.sub(r'\s+', '', str(value)).casefold() == 'mitarbeiter/tag']
    if len(headers) != 1:
        raise ConversionError("Die Beschriftung 'Mitarbeiter/Tag' konnte nicht eindeutig gefunden werden.")
    headerRow, labelColumn = headers[0]
    dayCount = calendar.monthrange(year, month)[1]
    candidates = []
    for r in range(max(0, headerRow - 2), min(len(rows), headerRow + 2)):
        for c in range(labelColumn + 1, SEARCH_COLUMNS - dayCount + 1):
            if [dayNumber(value) for value in rows[r][c:c + dayCount]] == list(range(1, dayCount + 1)):
                candidates.append((r, c))
    if len(candidates) != 1:
        raise ConversionError('Die Dienstplanstruktur konnte nicht erkannt werden: Die Tagesfolge ist unvollständig oder unplausibel.')
    employees = [r for r in range(headerRow + 1, len(rows) - 1)
                 if str(rows[r][labelColumn] or '').strip().casefold() == 'klein']
    if len(employees) != 1:
        raise ConversionError("Der Mitarbeiter 'Klein' konnte in dieser Datei nicht eindeutig gefunden werden.")
    employeeRow = employees[0]
    if rows[employeeRow + 1][labelColumn] not in (None, '', 'Klein'):
        raise ConversionError('Die zweite Dienstplanzeile für Klein konnte nicht erkannt werden.')
    return employeeRow, candidates[0][1], dayCount, candidates[0][0], headerRow

from dienstplan_converter.calendar_utils import outputFilename, splitMonth
from dienstplan_converter.models import DayEntry, MonthSchedule
import pytest


@pytest.mark.parametrize(('count', 'firstCount'), [(28, 14), (29, 15), (30, 15), (31, 16)])
def testMonthSplit(count: int, firstCount: int) -> None:
    days = tuple(DayEntry(day, 'Mo', None, None) for day in range(1, count + 1))
    first, second = splitMonth(days)
    assert [entry.day for entry in first] == list(range(1, firstCount + 1))
    assert [entry.day for entry in second] == list(range(firstCount + 1, count + 1))


@pytest.mark.parametrize(('month', 'name'), [(1, 'Januar'), (3, 'März'), (4, 'April'), (10, 'Oktober')])
def testFilename(month: int, name: str) -> None:
    assert outputFilename(MonthSchedule('Klein', 2026, month, ())) == f'Dienstplan_Klein_{name}_2026.pdf'

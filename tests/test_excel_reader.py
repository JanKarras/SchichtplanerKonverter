from pathlib import Path
from time import perf_counter
import pytest
from openpyxl import load_workbook
from dienstplan_converter.excel_reader import readSchedule

FIXTURES = sorted((Path(__file__).parent / 'fixtures').glob('*.xlsx'))


@pytest.mark.parametrize('inputPath', FIXTURES, ids=[p.name for p in FIXTURES])
def testRealFixtures(inputPath: Path) -> None:
    month = int(inputPath.stem[-2:])
    started = perf_counter()
    schedule = readSchedule(inputPath)
    assert perf_counter() - started < 10
    assert (schedule.employee, schedule.year, schedule.month) == ('Klein', 2026, month)
    assert len(schedule.days) == (30 if month in (4, 9) else 31)
    assert schedule.days[0].day == 1
    assert schedule.days[-1].day == len(schedule.days)
    expectedFirst = {1: (None, None), 4: ('SF', 'LSS'), 8: (None, 'SF'),
                     9: (None, 'Ber'), 10: (None, 'Mobs')}
    assert (schedule.days[0].primaryValue, schedule.days[0].secondaryValue) == expectedFirst[month]


def testFollowingMonthAndRealValues() -> None:
    schedule = readSchedule(FIXTURES[0])
    assert len(schedule.days) == 31
    assert schedule.days[-1].weekday == 'Sa'
    assert schedule.days[9].primaryValue == 'SF'
    assert schedule.days[9].secondaryValue == 'SF'
    assert schedule.days[0].primaryValue is None
    assert schedule.days[0].secondaryValue is None
    assert schedule.days[1].secondaryValue == 'U'


def testBlanksAndExtraData(sampleFile: Path) -> None:
    schedule = readSchedule(sampleFile)
    assert schedule.days[0].primaryValue == 'SF'
    assert schedule.days[0].secondaryValue == 'LSS'
    assert schedule.days[1].secondaryValue is None
    assert schedule.days[2].secondaryValue == 'VS+A'
    assert len(schedule.days) == 30
    assert not any(day.secondaryValue == 'IGNORE' for day in schedule.days)


def testVerticalAndHorizontalShift(sampleFile: Path) -> None:
    workbook = load_workbook(sampleFile)
    workbook.active.insert_rows(2, 3)
    workbook.active.insert_cols(1, 2)
    workbook.save(sampleFile)
    workbook.close()
    schedule = readSchedule(sampleFile)
    assert schedule.days[0].secondaryValue == 'LSS'
    assert schedule.month == 4

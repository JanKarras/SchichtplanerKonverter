from pathlib import Path
import pytest
from openpyxl import Workbook


@pytest.fixture
def sampleFile(tmp_path: Path) -> Path:
    workbook = Workbook()
    sheet = workbook.active
    sheet['N1'] = 'April 2026'
    sheet['B4'] = 'Mitarbeiter/Tag'
    sheet['B7'] = 'Klein'
    for day in range(1, 31):
        sheet.cell(3, day + 2, day)
    sheet['C7'] = 'SF'
    sheet['C8'] = 'LSS'
    sheet['E8'] = 'VS+A'
    sheet['AK8'] = 'IGNORE'
    path = tmp_path / 'plan.xlsx'
    workbook.save(path)
    workbook.close()
    return path

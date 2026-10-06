from pathlib import Path
import calendar
import datetime
import pytest
from pypdf import PdfReader
from reportlab.lib.pagesizes import A4, landscape
from dienstplan_converter.calendar_utils import WEEKDAY_NAMES, outputFilename
from dienstplan_converter.errors import ConversionError
from dienstplan_converter.models import DayEntry, MonthSchedule
from dienstplan_converter.pdf_renderer import renderPdf
from dienstplan_converter.main import convertFile


@pytest.mark.parametrize(('year', 'month'), [(2026, 2), (2028, 2), (2026, 4), (2026, 10)])
def testSingleLandscapePage(tmp_path: Path, year: int, month: int) -> None:
    days = tuple(DayEntry(day, WEEKDAY_NAMES[datetime.date(year, month, day).weekday()],
                          '07-15:30' if day == 28 else 'SF', 'VS+A')
                 for day in range(1, calendar.monthrange(year, month)[1] + 1))
    schedule = MonthSchedule('Klein', year, month, days)
    path = tmp_path / outputFilename(schedule)
    renderPdf(schedule, path)
    assert list(tmp_path.iterdir()) == [path]
    assert path.stat().st_size > 1000
    pdf = PdfReader(path)
    assert len(pdf.pages) == 1
    assert float(pdf.pages[0].mediabox.width) == pytest.approx(landscape(A4)[0], abs=0.01)
    assert float(pdf.pages[0].mediabox.height) == pytest.approx(landscape(A4)[1], abs=0.01)
    text = pdf.pages[0].extract_text()
    assert 'Klein' in text and 'VS+A' in text and f'{len(days):02}' in text


def testWorkflowAndOverwrite(sampleFile: Path) -> None:
    original = sampleFile.read_bytes()
    path = convertFile(sampleFile)
    assert path.name == 'Dienstplan_Klein_April_2026.pdf'
    assert path.parent == sampleFile.parent
    path.write_bytes(b'old')
    assert convertFile(sampleFile) == path
    assert len(PdfReader(path).pages) == 1
    assert sampleFile.read_bytes() == original


def testUnwritableOutput(sampleFile: Path) -> None:
    path = sampleFile.parent / 'Dienstplan_Klein_April_2026.pdf'
    path.mkdir()
    with pytest.raises(ConversionError, match='PDF konnte nicht gespeichert'):
        convertFile(sampleFile)


def testRejectIncompleteModel(tmp_path: Path) -> None:
    with pytest.raises(ConversionError, match='unvollständig'):
        renderPdf(MonthSchedule('Klein', 2026, 4, ()), tmp_path / 'invalid.pdf')

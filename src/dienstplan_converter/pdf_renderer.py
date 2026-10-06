import calendar
from io import BytesIO
from pathlib import Path
from tempfile import NamedTemporaryFile

from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas

from .calendar_utils import MONTH_NAMES, splitMonth
from .errors import ConversionError
from .error_log import logUnexpectedError
from .models import DayEntry, MonthSchedule
from .theme import DEFAULT_THEME, PdfTheme


def drawText(canvas: Canvas, text: str, x: float, y: float, width: float,
             height: float, font: str, size: float, theme: PdfTheme) -> None:
    available = width - 2 * theme.cellPadding
    textWidth = stringWidth(text, font, size)
    fittedSize = min(size, size * available / textWidth) if textWidth else size
    canvas.setFillColor(theme.textColor)
    canvas.setFont(font, fittedSize)
    canvas.drawCentredString(x + width / 2, y + (height - fittedSize) / 2 + fittedSize * 0.18, text)


def drawTable(canvas: Canvas, days: tuple[DayEntry, ...], top: float,
              width: float, theme: PdfTheme) -> None:
    dayWidth = (width - theme.labelWidth) / len(days)
    totalHeight = sum(theme.rowHeights)
    left = theme.margin
    for index, day in enumerate(days):
        x = left + theme.labelWidth + index * dayWidth
        canvas.setFillColor(theme.weekendColor if day.weekday in ('Sa', 'So') else theme.headerColor)
        canvas.rect(x, top - totalHeight if day.weekday in ('Sa', 'So') else top - sum(theme.rowHeights[:2]),
                    dayWidth, totalHeight if day.weekday in ('Sa', 'So') else sum(theme.rowHeights[:2]), stroke=0, fill=1)
        values = (f'{day.day:02}', day.weekday, day.primaryValue or '', day.secondaryValue or '')
        y = top
        for row, (value, height) in enumerate(zip(values, theme.rowHeights)):
            y -= height
            size = (theme.daySize, theme.weekdaySize, theme.valueSize, theme.valueSize)[row]
            font = theme.boldFont if row != 1 or day.weekday in ('Sa', 'So') else theme.font
            drawText(canvas, value, x, y, dayWidth, height, font, size, theme)
    drawText(canvas, 'Mitarbeiter / Tag', left, top - theme.rowHeights[0],
             theme.labelWidth, theme.rowHeights[0], theme.boldFont, theme.labelSize, theme)
    drawText(canvas, 'Klein', left, top - totalHeight, theme.labelWidth,
             sum(theme.rowHeights[2:]), theme.boldFont, theme.employeeSize, theme)
    canvas.setStrokeColor(theme.lineColor)
    canvas.setLineWidth(theme.lineWidth)
    for index in range(len(days)):
        x = left + theme.labelWidth + index * dayWidth
        canvas.line(x, top, x, top - totalHeight)
    y = top
    for row, height in enumerate(theme.rowHeights[:-1]):
        y -= height
        canvas.line(left + theme.labelWidth if row == 2 else left, y, left + width, y)
    canvas.setLineWidth(theme.outerLineWidth)
    canvas.rect(left, top - totalHeight, width, totalHeight)


def renderPdf(schedule: MonthSchedule, outputPath: Path, theme: PdfTheme = DEFAULT_THEME) -> Path:
    expectedDays = calendar.monthrange(schedule.year, schedule.month)[1]
    if schedule.employee != 'Klein' or [day.day for day in schedule.days] != list(range(1, expectedDays + 1)):
        raise ConversionError('Der Monatsdienstplan ist unvollständig oder unplausibel.')
    pageWidth, pageHeight = landscape(A4)
    tableHeight = sum(theme.rowHeights)
    if theme.titleGap + 2 * tableHeight + theme.tableGap + 2 * theme.margin > pageHeight:
        raise ConversionError('Die gewählten Layoutwerte passen nicht auf eine A4-Seite.')
    buffer = BytesIO()
    canvas = Canvas(buffer, pagesize=landscape(A4))
    title = f'Dienstplan Klein – {MONTH_NAMES[schedule.month]} {schedule.year}'
    canvas.setTitle(title)
    canvas.setAuthor('DienstplanConverter')
    drawText(canvas, title, theme.margin, pageHeight - theme.margin - 30,
             pageWidth - 2 * theme.margin, 30, theme.boldFont, theme.titleSize, theme)
    top = pageHeight - theme.margin - theme.titleGap
    for days in splitMonth(schedule.days):
        canvas.setFillColor(theme.textColor)
        canvas.setFont(theme.boldFont, theme.sectionSize)
        canvas.drawString(theme.margin, top + 10,
                          f'{days[0].day:02}.{schedule.month:02}.{schedule.year} – '
                          f'{days[-1].day:02}.{schedule.month:02}.{schedule.year}')
        drawTable(canvas, days, top, pageWidth - 2 * theme.margin, theme)
        top -= tableHeight + theme.tableGap
    canvas.showPage()
    canvas.save()
    savePdf(buffer.getvalue(), outputPath)
    return outputPath


def savePdf(content: bytes, outputPath: Path) -> None:
    """Erst vollständig schreiben, dann ersetzen: bestehende PDFs bleiben bei Fehlern erhalten."""
    temporaryPath = None
    try:
        with NamedTemporaryFile(dir=outputPath.parent, prefix='.dienstplan-', suffix='.tmp', delete=False) as stream:
            temporaryPath = Path(stream.name)
            stream.write(content)
        temporaryPath.replace(outputPath)
    except OSError as error:
        raise ConversionError('Die PDF konnte nicht gespeichert werden. Bitte prüfen Sie, ob die bestehende PDF noch geöffnet ist oder der Ordner schreibgeschützt ist.') from error
    finally:
        if temporaryPath is not None:
            try:
                temporaryPath.unlink(missing_ok=True)
            except OSError:
                # Cleanup must not replace the useful save error with a raw exception.
                logUnexpectedError()

"""Alle PDF-Layoutwerte in Punkten (72 Punkte = 1 Zoll)."""
from dataclasses import dataclass
from reportlab.lib.colors import HexColor, Color


@dataclass(frozen=True)
class PdfTheme:
    margin: float = 18
    titleSize: float = 26
    sectionSize: float = 16
    daySize: float = 22
    weekdaySize: float = 15
    valueSize: float = 21
    labelSize: float = 14
    employeeSize: float = 24
    labelWidth: float = 112
    rowHeights: tuple[float, ...] = (36, 28, 82, 82)
    tableGap: float = 36
    titleGap: float = 64
    cellPadding: float = 3
    lineWidth: float = 1.0
    outerLineWidth: float = 1.6
    textColor: Color = HexColor('#202830')
    lineColor: Color = HexColor('#38424c')
    headerColor: Color = HexColor('#f0f2f4')
    weekendColor: Color = HexColor('#e1e5e8')
    font: str = 'Helvetica'
    boldFont: str = 'Helvetica-Bold'


DEFAULT_THEME = PdfTheme()

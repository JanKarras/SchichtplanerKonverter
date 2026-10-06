"""Alle PDF-Layoutwerte in Punkten (72 Punkte = 1 Zoll)."""
from dataclasses import dataclass
from reportlab.lib.colors import HexColor, Color


@dataclass(frozen=True)
class PdfTheme:
    margin: float = 28
    titleSize: float = 23
    sectionSize: float = 12
    daySize: float = 17
    weekdaySize: float = 12
    valueSize: float = 16
    labelSize: float = 13
    labelWidth: float = 112
    rowHeights: tuple[float, ...] = (34, 26, 62, 62)
    tableGap: float = 48
    titleGap: float = 62
    cellPadding: float = 3
    lineWidth: float = 0.7
    outerLineWidth: float = 1.2
    textColor: Color = HexColor('#202830')
    lineColor: Color = HexColor('#38424c')
    headerColor: Color = HexColor('#f0f2f4')
    weekendColor: Color = HexColor('#e1e5e8')
    font: str = 'Helvetica'
    boldFont: str = 'Helvetica-Bold'


DEFAULT_THEME = PdfTheme()

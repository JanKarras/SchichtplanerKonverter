"""Farbpriorität und Textkontrast ausschließlich anhand neutraler Modellwerte."""
from reportlab.lib.colors import Color, HexColor, white, black

from .models import DayEntry
from .theme import PdfTheme


def dayBackgrounds(day: DayEntry, theme: PdfTheme) -> tuple[Color, ...]:
    fallback = theme.weekendColor if day.weekday in ('Sa', 'So') else white
    return tuple(HexColor(value) if value is not None else fallback for value in
                 (day.headerColor, day.weekdayColor, day.primaryColor, day.secondaryColor))


def contrastingText(background: Color) -> Color:
    channels = (background.red, background.green, background.blue)
    linear = tuple(value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
                   for value in channels)
    luminance = sum(value * weight for value, weight in zip(linear, (0.2126, 0.7152, 0.0722)))
    blackContrast = (luminance + 0.05) / 0.05
    whiteContrast = 1.05 / (luminance + 0.05)
    return black if blackContrast >= whiteContrast else white

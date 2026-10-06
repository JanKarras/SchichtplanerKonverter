from pathlib import Path
from unittest.mock import Mock
import pytest
from reportlab.lib.colors import HexColor, black, white
from dienstplan_converter.models import DayEntry
from dienstplan_converter.pdf_colors import contrastingText, dayBackgrounds
from dienstplan_converter.pdf_renderer import drawTable
from dienstplan_converter.theme import DEFAULT_THEME


@pytest.mark.parametrize(('color', 'expected'), [('#000000', white), ('#FFFFFF', black),
    ('#123456', white), ('#FF0000', black), ('#CC66FF', black), ('#92D050', black)])
def testContrast(color: str, expected) -> None:
    assert contrastingText(HexColor(color)) == expected


def testBackgroundPriority() -> None:
    weekend = DayEntry(1, 'Sa', None, None, '#FFFFFF', '#FF0000', '#000000')
    colors = dayBackgrounds(weekend, DEFAULT_THEME)
    assert colors == (white, HexColor('#FF0000'), black, DEFAULT_THEME.weekendColor)
    assert dayBackgrounds(DayEntry(2, 'Mo', None, None), DEFAULT_THEME) == (white,) * 4


def testSeparateCellsAndTextContrast() -> None:
    day = DayEntry(1, 'Mo', 'SF', 'Berlin', '#123456', '#ABCDEF', '#000000', '#FFFFFF')
    canvas = Mock()
    drawTable(canvas, (day,), 500, 700, DEFAULT_THEME)
    # Four separate filled rectangles with the approved row heights.
    rectangles = [call for call in canvas.rect.call_args_list if call.kwargs.get('fill') == 1]
    assert len(rectangles) == 4
    assert [call.args[3] for call in rectangles] == list(DEFAULT_THEME.rowHeights)
    fills = [call.args[0] for call in canvas.setFillColor.call_args_list]
    assert fills[:8] == [HexColor('#123456'), white, HexColor('#ABCDEF'), black,
                         black, white, white, black]

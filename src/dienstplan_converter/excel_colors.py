"""Excel-Füllungen als neutrale RGB-Werte, unabhängig vom PDF-Renderer."""
import colorsys
import re
from xml.etree import ElementTree

from openpyxl.styles.colors import COLOR_INDEX
from openpyxl.styles.fills import PatternFill

THEME_NAMES = ('lt1', 'dk1', 'lt2', 'dk2', 'accent1', 'accent2', 'accent3',
               'accent4', 'accent5', 'accent6', 'hlink', 'folHlink')
DRAWING_NAMESPACE = 'http://schemas.openxmlformats.org/drawingml/2006/main'


def readTheme(themeXml: bytes | None) -> tuple[str | None, ...]:
    if not isinstance(themeXml, bytes):
        return ()
    root = ElementTree.fromstring(themeXml)
    scheme = root.find(f'.//{{{DRAWING_NAMESPACE}}}clrScheme')
    if scheme is None:
        return ()
    palette = []
    for name in THEME_NAMES:
        entry = scheme.find(f'{{{DRAWING_NAMESPACE}}}{name}')
        color = entry[0] if entry is not None and len(entry) else None
        value = None if color is None else color.get('lastClr') if color.tag.endswith('sysClr') else color.get('val')
        palette.append(value)
    return tuple(palette)


def applyTint(rgb: str, tint: float) -> str:
    if not tint:
        return '#' + rgb.upper()
    channels = tuple(int(rgb[index:index + 2], 16) / 255 for index in (0, 2, 4))
    hue, luminance, saturation = colorsys.rgb_to_hls(*channels)
    # OOXML applies tint to HLS luminance; normalized 0..1 avoids intermediate rounding.
    luminance = luminance * (1 + tint) if tint < 0 else luminance * (1 - tint) + tint
    result = colorsys.hls_to_rgb(hue, luminance, saturation)
    return '#' + ''.join(f'{round(max(0, min(1, component)) * 255):02X}' for component in result)


def normalizeFill(fill: PatternFill | None, theme: tuple[str | None, ...],
                  indexed: tuple[str, ...] = COLOR_INDEX) -> str | None:
    if fill is None or getattr(fill, 'patternType', None) != 'solid':
        return None
    color = fill.fgColor
    value = None
    if color.type == 'rgb':
        value = color.rgb
    elif color.type == 'theme' and 0 <= color.theme < len(theme):
        value = theme[color.theme]
    elif color.type == 'indexed' and 0 <= color.indexed < min(64, len(indexed)):
        # Indices 64/65 are system-dependent foreground/background colors.
        value = indexed[color.indexed]
    if not isinstance(value, str) or not re.fullmatch(r'(?:[0-9a-fA-F]{2}){3,4}', value):
        return None
    # Excel cell fills ignore the alpha byte, including openpyxl's default 00.
    return applyTint(value[-6:], color.tint)

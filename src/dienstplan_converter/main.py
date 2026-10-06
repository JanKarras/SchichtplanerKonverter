"""Minimaler Windows-Workflow: Argument oder Dateiauswahl, danach Meldung."""
import sys
from pathlib import Path
from typing import Any

from .dialogs import createRoot, chooseFile, showInfo, showError

from .calendar_utils import outputFilename
from .errors import ConversionError
from .excel_reader import readSchedule
from .pdf_renderer import renderPdf
from .error_log import logUnexpectedError


def convertFile(inputPath: Path) -> Path:
    schedule = readSchedule(inputPath)
    return renderPdf(schedule, inputPath.parent / outputFilename(schedule))


def runApplication(arguments: list[str], root: Any) -> int:
    try:
        if len(arguments) > 1:
            raise ConversionError('Bitte ziehen Sie genau eine .xlsx-Datei auf das Programm.')
        selected = arguments[0] if arguments else chooseFile(root)
        if not selected:
            return 0
        outputPath = convertFile(Path(selected))
        showInfo(root, f'Dienstplan erfolgreich erstellt.\n\n{outputPath}')
        return 0
    except ConversionError as error:
        showError(root, str(error))
        return 1
    except Exception:
        logPath = logUnexpectedError()
        detail = f'\n\nTechnische Details: {logPath}' if logPath else ''
        showError(root, 'Ein unerwarteter Fehler ist aufgetreten.' + detail)
        return 1


def main() -> int:
    root = None
    try:
        root = createRoot()
        return runApplication(sys.argv[1:], root)
    except Exception:
        logUnexpectedError()
        # Native fallback if Tk itself cannot start on Windows.
        if sys.platform == 'win32':
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, 'Die Anwendung konnte nicht gestartet werden. Bitte prüfen Sie die lokale Logdatei.', 'DienstplanConverter', 0x10)
        else:
            print('Der Dateidialog benötigt eine grafische Umgebung mit Tk.', file=sys.stderr)
        return 1
    finally:
        if root is not None:
            try:
                root.destroy()
            except Exception:
                # A Tk cleanup failure must not escape a windowed application.
                logUnexpectedError()


if __name__ == '__main__':
    raise SystemExit(main())

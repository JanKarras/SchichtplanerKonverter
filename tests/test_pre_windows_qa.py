import os
from pathlib import Path
from unittest.mock import Mock
import pytest

from dienstplan_converter import main as application
from dienstplan_converter.errors import ConversionError
from dienstplan_converter import pdf_renderer


@pytest.mark.parametrize('mode', ['success', 'expectedError', 'unexpectedError', 'destroyError'])
def testExitPaths(monkeypatch, tmp_path: Path, mode: str) -> None:
    root = Mock()
    path = tmp_path / 'Dienstpläne ÄÖÜ' / 'April für Klein.xlsx'
    monkeypatch.setattr(application, 'createRoot', lambda: root)
    monkeypatch.setattr(application.sys, 'argv', ['DienstplanConverter.exe', str(path)])
    converter = Mock(return_value=path.with_suffix('.pdf'))
    if mode == 'expectedError':
        converter.side_effect = ConversionError('Testfehler')
    elif mode == 'unexpectedError':
        converter.side_effect = RuntimeError('Testfehler')
    elif mode == 'destroyError':
        root.destroy.side_effect = RuntimeError('Tk beendet')
    monkeypatch.setattr(application, 'convertFile', converter)
    monkeypatch.setattr(application, 'chooseFile', Mock(side_effect=AssertionError('Dialog trotz Argument')))
    info, error = Mock(), Mock()
    monkeypatch.setattr(application, 'showInfo', info)
    monkeypatch.setattr(application, 'showError', error)
    monkeypatch.setattr(application, 'logUnexpectedError', Mock(return_value=tmp_path / 'error.log'))
    assert application.main() == (1 if mode in ('expectedError', 'unexpectedError') else 0)
    converter.assert_called_once_with(path)
    root.destroy.assert_called_once()
    assert error.call_count == (1 if mode in ('expectedError', 'unexpectedError') else 0)
    assert info.call_count == (1 if mode in ('success', 'destroyError') else 0)


def testUnicodeAndSpaces(sampleFile: Path, tmp_path: Path) -> None:
    directory = tmp_path / 'Dienstpläne Müller ÄÖÜ ß'
    directory.mkdir()
    path = directory / 'April für Klein.XLSX'
    original = sampleFile.read_bytes()
    path.write_bytes(original)
    output = application.convertFile(path)
    assert output == directory / 'Dienstplan_Klein_April_2026.pdf'
    assert output.is_file()
    assert path.read_bytes() == original


@pytest.mark.skipif(os.name == 'nt', reason='POSIX-Rechteprüfung; Windows-Ordnerrechte erfordern ACLs.')
def testReadOnlyDirectory(sampleFile: Path) -> None:
    directory = sampleFile.parent
    previousMode = directory.stat().st_mode
    directory.chmod(0o555)
    try:
        with pytest.raises(ConversionError, match='PDF konnte nicht gespeichert'):
            application.convertFile(sampleFile)
        assert not list(directory.glob('*.pdf'))
    finally:
        directory.chmod(previousMode)


def testCleanupDoesNotMaskSaveError(monkeypatch, tmp_path: Path) -> None:
    target = tmp_path / 'existing.pdf'
    target.write_bytes(b'original')
    monkeypatch.setattr(Path, 'replace', Mock(side_effect=PermissionError('target locked')))
    monkeypatch.setattr(Path, 'unlink', Mock(side_effect=PermissionError('cleanup locked')))
    logged = Mock()
    monkeypatch.setattr(pdf_renderer, 'logUnexpectedError', logged)
    with pytest.raises(ConversionError, match='PDF konnte nicht gespeichert'):
        pdf_renderer.savePdf(b'new', target)
    assert target.read_bytes() == b'original'
    logged.assert_called_once()

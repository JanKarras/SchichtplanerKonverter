from pathlib import Path
from unittest.mock import Mock
from dienstplan_converter import main as application


def testCancelAndFileSelection(monkeypatch, sampleFile: Path) -> None:
    root = Mock()
    info = Mock()
    monkeypatch.setattr(application, 'showInfo', info)
    monkeypatch.setattr(application, 'chooseFile', lambda root: '')
    assert application.runApplication([], root) == 0
    info.assert_not_called()
    monkeypatch.setattr(application, 'chooseFile', lambda root: str(sampleFile))
    assert application.runApplication([], root) == 0
    assert 'Dienstplan_Klein_April_2026.pdf' in info.call_args.args[1]


def testArgumentsAndExpectedErrors(monkeypatch, sampleFile: Path) -> None:
    error = Mock()
    monkeypatch.setattr(application, 'showError', error)
    monkeypatch.setattr(application, 'showInfo', Mock())
    assert application.runApplication([str(sampleFile)], Mock()) == 0
    assert application.runApplication(['a.xlsx', 'b.xlsx'], Mock()) == 1
    assert 'genau eine' in error.call_args.args[1]
    assert application.runApplication(['missing.xlsx'], Mock()) == 1
    assert 'existiert nicht' in error.call_args.args[1]


def testUnexpectedErrorLogging(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv('LOCALAPPDATA', str(tmp_path))
    monkeypatch.setattr(application, 'convertFile', Mock(side_effect=RuntimeError('technical test detail')))
    error = Mock()
    monkeypatch.setattr(application, 'showError', error)
    assert application.runApplication(['a.xlsx'], Mock()) == 1
    logPath = tmp_path / 'DienstplanConverter' / 'DienstplanConverter.log'
    assert 'technical test detail' in logPath.read_text()
    assert 'technical test detail' not in error.call_args.args[1]


def testRootCleanup(monkeypatch) -> None:
    root = Mock()
    monkeypatch.setattr(application, 'createRoot', lambda: root)
    monkeypatch.setattr(application.sys, 'argv', ['converter'])
    monkeypatch.setattr(application, 'chooseFile', lambda root: '')
    assert application.main() == 0
    root.destroy.assert_called_once()

from pathlib import Path
from unittest.mock import Mock
import pytest
from dienstplan_converter.errors import ConversionError
from dienstplan_converter.main import convertFile


def testLockedTargetLeavesExistingPdf(monkeypatch, sampleFile: Path) -> None:
    target = sampleFile.parent / 'Dienstplan_Klein_April_2026.pdf'
    target.write_bytes(b'existing pdf')
    monkeypatch.setattr(Path, 'replace', Mock(side_effect=PermissionError('locked')))
    with pytest.raises(ConversionError, match='noch geöffnet'):
        convertFile(sampleFile)
    assert target.read_bytes() == b'existing pdf'
    assert not list(sampleFile.parent.glob('.dienstplan-*.tmp'))

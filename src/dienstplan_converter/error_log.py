import os
import traceback
from datetime import datetime
from pathlib import Path


def logUnexpectedError() -> Path | None:
    """Lokales Log, maximal ungefähr 256 KiB; kein Netzwerkzugriff."""
    locations = [Path(os.environ.get('LOCALAPPDATA', str(Path.home()))) / 'DienstplanConverter', Path.cwd()]
    details = f'\n{datetime.now().isoformat()}\n{traceback.format_exc()}'
    for folder in locations:
        try:
            folder.mkdir(parents=True, exist_ok=True)
            path = folder / 'DienstplanConverter.log'
            mode = 'w' if path.exists() and path.stat().st_size > 256 * 1024 else 'a'
            with path.open(mode, encoding='utf-8') as stream:
                stream.write(details)
            return path
        except OSError:
            continue
    return None

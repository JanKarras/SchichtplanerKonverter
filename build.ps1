$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
if ($env:OS -ne "Windows_NT") { throw "Der Windows-Build muss unter Windows laufen." }
$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    py -3.12 -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw "Python 3.12 mit Tkinter muss installiert sein." }
}
& $python -c "import tkinter; import tkinter.filedialog; import tkinter.messagebox"
if ($LASTEXITCODE -ne 0) { throw "Tkinter fehlt. Python 3.12 mit Tcl/Tk installieren." }
& $python -m pip install -e ".[dev]"
if ($LASTEXITCODE -ne 0) { throw "Installation fehlgeschlagen." }
& $python -m pytest
if ($LASTEXITCODE -ne 0) { throw "Tests fehlgeschlagen; Build abgebrochen." }
& $python -m PyInstaller --noconfirm --clean --onefile --windowed --name DienstplanConverter --paths src windows_entry.py
if ($LASTEXITCODE -ne 0) { throw "PyInstaller-Build fehlgeschlagen." }
Write-Host "Fertig: $PSScriptRoot\dist\DienstplanConverter.exe"

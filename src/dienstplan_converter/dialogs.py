"""Tk wird erst beim tatsächlichen Dialogstart benötigt."""
from typing import Any


def createRoot() -> Any:
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    return root


def chooseFile(root: Any) -> str:
    from tkinter import filedialog
    return filedialog.askopenfilename(parent=root, title='Excel-Dienstplan auswählen',
                                      filetypes=[('Excel-Dienstplan', '*.xlsx')])


def showInfo(root: Any, message: str) -> None:
    from tkinter import messagebox
    messagebox.showinfo('DienstplanConverter', message, parent=root)


def showError(root: Any, message: str) -> None:
    from tkinter import messagebox
    messagebox.showerror('DienstplanConverter', message, parent=root)

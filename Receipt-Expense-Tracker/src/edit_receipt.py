import sys

from pathlib import Path
import subprocess
#subprocess function: Python. (n.d.). subprocess — Subprocess management — Python 3.8.5 documentation. Docs.python.org. https://docs.python.org/3/library/subprocess.html

from tkinter import *
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import Label
from PIL import Image, ImageTk

import parsing_engine 

#pathlib function: pathlib — Object-oriented filesystem paths — Python 3.9.4 documentation. (n.d.). Docs.python.org. https://docs.python.org/3/library/pathlib.html
SRC_folder = Path(__file__).resolve().parent
main_folder = SRC_folder.parent.parent

def open_edit_receipt_page(upload_page):
    app = tk.Toplevel(upload_page)
    # setting title and basic size to the page
    app.title("Receipt Validation and Manual Edit")
    app.geometry("600x650")
    app.configure(bg="#ceecf5")

    def go_back():
        app.destroy()
        upload_page.deiconify()


    app.protocol("WM_DELETE_WINDOW", go_back)
    


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
import edit_receipt

#pathlib function: pathlib — Object-oriented filesystem paths — Python 3.9.4 documentation. (n.d.). Docs.python.org. https://docs.python.org/3/library/pathlib.html
SRC_folder = Path(__file__).resolve().parent
main_folder = SRC_folder.parent.parent


select_image = None

def open_upload_page(main_menu):
    app = tk.Toplevel(main_menu)
    app.title("Receipt Expense Tracker - Upload Receipt")
    app.minsize(600, 760)
    app.configure(bg="#ceecf5")

    #upload image function: https://www.geeksforgeeks.org/python/browse-upload-display-image-in-tkinter/
    def upload_image():
        global select_image

        file_types = [("Image files", "*.png;*.jpg;*.jpeg")]
        path = tk.filedialog.askopenfilename(filetypes=file_types)

        # if file is selected
        if len(path):
            select_image = path

            img = Image.open(path)
            img = img.resize((260, 260))
            pic = ImageTk.PhotoImage(img)

            # re-sizing the app window in order to fit picture
            app.geometry("650x520")
            label.config(image=pic, text="", width=260, height=260)
            label.image = pic

            return path

        # if no file is selected, display below message
        else:
            print("No file is chosen !")

    def confirm_image():
        global select_image

        if select_image is not None:
            extracted_data = parsing_engine.upload_and_parse_receipt(select_image)

            print(extracted_data)

            app.withdraw()  # Hide the upload page
            edit_receipt.open_edit_receipt_page(app, extracted_data)  # Open the edit receipt page

        else:
            print("\n[ERROR] Please click 'Locate Image' and select a file first!")

    def go_back():
        app.destroy()
        main_menu.deiconify()


    title_Label = tk.Label(
        app,
        text=" Upload Receipt Image",
        font=("Ink Free", 30, "bold"),
        bg="#ceecf5",
        relief=RAISED,
        bd=15
    )
    title_Label.pack(pady=15)

    
    subtitle_Label = tk.Label(
        app,
        text="Please select a receipt image",
        font=("Ink Free", 15, "bold"),
        bg="#ceecf5"
    )
    subtitle_Label.pack(pady=10)

    
    label = tk.Label(
        app,
        text="No Image Selected",
        font=("Ink Free", 14, "bold"),
        bg="white",
        width=40,
        height=15,
        relief=SUNKEN,
        bd=3
    )
    label.pack(pady=15)
 

    uploadButton = tk.Button(
        app,
        text="Locate Image",
        width=20,
        height=2,
        font=("Ink Free", 13, "bold"),
        bg="#90c9de",
        command=upload_image
    )
    uploadButton.pack(pady=10)

    
    confirmButton = tk.Button(
        app,
        text="Confirm Image",
        width=20,
        height=2,
        font=("Ink Free", 13, "bold"),
        bg="#90c9de",
        command=confirm_image
    )
    confirmButton.pack(pady=10)

    goBackButton = tk.Button(
        app,
        text="Go Back",
        width=20,
        height=2,
        font=("Ink Free", 13, "bold"),
        bg="#90c9de",
        command=go_back
    )

    goBackButton.pack(pady=10)
    app.protocol("WM_DELETE_WINDOW", go_back)
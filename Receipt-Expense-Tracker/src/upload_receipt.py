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


select_image = None
#upload image function: https://www.geeksforgeeks.org/python/browse-upload-display-image-in-tkinter/
def upload_image():
    global select_image

    file_types = [("Image files", "*.png;*.jpg;*.jpeg")]
    path = tk.filedialog.askopenfilename(filetypes=file_types)

    # if file is selected
    if len(path):
        select_image = path

        img = Image.open(path)
        img = img.resize((200, 200))
        pic = ImageTk.PhotoImage(img)

        # re-sizing the app window in order to fit picture
        app.geometry("560x300")
        label.config(image=pic)
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

    else:
        print("\n[ERROR] Please click 'Locate Image' and select a file first!")



# defining tkinter object
app = tk.Tk()

# setting title and basic size to our App
app.title("GeeksForGeeks Image Viewer")
app.geometry("560x270")

# adding background color to our upload button
app.option_add("*Label*Background", "white")
app.option_add("*Button*Background", "lightgreen")

label = tk.Label(app)
label.pack(pady=10)

# defining our upload buttom
uploadButton = tk.Button(app, text="Locate Image", command=upload_image)
uploadButton.pack(side=tk.BOTTOM, pady=20)

# defining our confirm buttom
confirmButton = tk.Button(app, text="Confirm Image", command=confirm_image)
confirmButton.pack(side=tk.BOTTOM, pady=20)

app.mainloop()

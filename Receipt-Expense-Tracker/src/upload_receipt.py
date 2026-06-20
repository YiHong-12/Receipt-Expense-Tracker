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

def open_upload_page(main_menu):
    app = tk.Toplevel(main_menu)
    # setting title and basic size to the page
    app.title("Receipt Upload")
    app.geometry("600x650")
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
            img = img.resize((200, 220))
            pic = ImageTk.PhotoImage(img)

            # re-sizing the app window in order to fit picture
            app.geometry("650x520")
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

    def go_back():
        app.destroy()
        main_menu.deiconify()


    main_frame=tk.Frame(
        app,
        bg="white",bd=2,relief="ridge"
    )
    main_frame.pack(padx=30,pady=25,fill="both",expand=True) #Adding frame for image upload UI

    #Main Title 
    title_Label=tk.Label(main_frame,text="Upload Receipt Image",
                     font=("Free Ink",24,"bold"),bg="white",fg="#1f4e79")
    title_Label.pack(pady=(25,5)) 

    #Subtitle
    subtitle_Label=tk.Label(
    main_frame,text="Please select a receipt image",font=("Free Ink",11),bg="white",fg="#555555"
    )
    subtitle_Label.pack(pady=(0,20))

    #adding frame for buttons
    button_frame=tk.Frame(main_frame,bg="white")
    button_frame.pack(pady=5)

    label = tk.Label(app)
    label.pack(pady=10)

        # defining our go back buttom
    goBackButton = tk.Button(
        button_frame,
        text="Go Back",
        font=("Free Ink", 12, "bold"),
        bg="#f44336",
        fg="white",
        width=16,
        height=2,
        bd=0,
        command=go_back)
    goBackButton.pack(side=tk.BOTTOM, pady=20)


    # defining our confirm buttom
    confirmButton = tk.Button(
        button_frame,
        text="Confirm Image",
        font=("Free Ink", 12, "bold"),
        bg="#4caf50",
        fg="white",
        width=16,
        height=2,
        bd=0,
        command=confirm_image)
    confirmButton.pack(side=tk.BOTTOM, pady=20)

    # defining our upload buttom
    uploadButton = tk.Button(
        button_frame, text="Locate Image",
        font=("Free Ink",12,"bold"),
        bg="#4da3d9",
        fg="white",
        width=16,
        height=2,
        bd=0, 
        command=upload_image)
    uploadButton.pack(side=tk.BOTTOM, pady=20)

    app.protocol("WM_DELETE_WINDOW", go_back)
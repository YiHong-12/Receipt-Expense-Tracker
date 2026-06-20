import sys

from pathlib import Path
import subprocess
#subprocess function: Python. (n.d.). subprocess — Subprocess management — Python 3.8.5 documentation. Docs.python.org. https://docs.python.org/3/library/subprocess.html

from tkinter import *
import tkinter as tk
from tkinter import messagebox

import upload_receipt
import dashboard
import history
import edit

#pathlib function: pathlib — Object-oriented filesystem paths — Python 3.9.4 documentation. (n.d.). Docs.python.org. https://docs.python.org/3/library/pathlib.html
SRC_folder = Path(__file__).resolve().parent
main_folder = SRC_folder.parent.parent

def run_python_file(file_name):

    subprocess.run(
        [sys.executable, str(SRC_folder / file_name)],
        cwd=str(main_folder)
    )

def imp_upload():
    messagebox.showinfo(title='Loading Page', message='Navigating to Receipt Capture Module...')
    window.withdraw()  # Hide the main menu window
    upload_receipt.open_upload_page(window)

def imp_dashboard():
    messagebox.showinfo(title='Loading Page', message='Navigating to Dashboard...')
    window.withdraw()  # Hide the main menu window
    dashboard.open_dashboard_page(window)

def imp_history():
    messagebox.showinfo(title='Loading Page', message='Navigating to Transaction History...')
    window.withdraw()  # Hide the main menu window
    history.open_history_page(window)

def imp_Edit():
    messagebox.showinfo(title='Loading Page', message='Navigating to Manual Edit Module...')
    window.withdraw()  # Hide the main menu window
    edit.open_edit_page(window)

def Exit():
    if messagebox.askyesno(title='Exit ?',message="Do you want to exit the program?"):
        print("Thank you for using Receipt Expense Tracker!")
        window.destroy()
    else:
        pass

window = Tk()
window.title("Receipt Expense Tracker")
window.geometry("600x650")
window.configure(bg="#ceecf5")

title1=Label(window,
            text=" Receipt Expense Tracker",
            font = ("Ink Free",30,"bold"),
            bg="#ceecf5",relief=RAISED,bd=15)
title1.place(x=60,y=10)


subtitle1=Label(window,text="Please select the function you need"
                ,font=("Ink Free",15,"bold"))                
subtitle1.place(x=130,y=100)

bt_upload=Button(window,text="1) Upload Receipt",
                 width=20,height=2,
                 font=("Ink Free", 13,"bold"),
                 bg="#90c9de",command=imp_upload)#upload command later
bt_upload.place(x=200,y=150)

bt_dashboard=Button(window,text="2) Open Dashboard",
                 width=20,height=2,
                 font=("Ink Free", 13,"bold"),
                 bg="#90c9de",command=imp_dashboard)#upload command later
bt_dashboard.place(x=200,y=230)
                 

bt_history=Button(window,text="3) Check History",
                 width=20,height=2,
                 font=("Ink Free", 13,"bold"),
                 bg="#90c9de",command=imp_history)#upload command later
bt_history.place(x=200,y=310)

bt_Edit=Button(window,text="4) Manual Edit",
                 width=20,height=2,
                 font=("Ink Free", 13,"bold"),
                 bg="#90c9de",command=imp_Edit)#upload command later
bt_Edit.place(x=200,y=390)

bt_exit=Button(window,text="5) Exit",
                 width=20,height=2,
                 font=("Ink Free", 13,"bold"),
                 bg="#90c9de",command=Exit)#upload command later
bt_exit.place(x=200,y=470)
            
window.mainloop()
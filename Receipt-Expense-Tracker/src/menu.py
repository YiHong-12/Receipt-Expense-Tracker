import sys
import tf_keras

sys.modules['tensorflow.keras'] = tf_keras
sys.modules['keras'] = tf_keras

import keras_ocr
import math

import subprocess

from tkinter import *
import tkinter as tk
from tkinter import messagebox


def imp_upload():
    messagebox.showinfo(title='Loading Page',message='Navigating to Receipt Capture Module...')
    subprocess.run(["python","receipt_capture,py"])

def imp_dasgboard():
    messagebox.showinfo(title='Loading Page',message='Navigating to Dashboard...')
    subprocess.run(["python","dashboard.py"])

def imp_history():
    messagebox.showinfo(title='Loading Page',message='Navigating to Transaction History...')
    subprocess.run(["python","categorize.py"])

def imp_Edit():
    messagebox.showinfo(title='Loading Page',message='Navigating to Manual Edit Module...')
    subprocess.run(["python","validation.py"])

def Exit():
    if messagebox.askyesno(title='Exit ?',message="Do you want to exit the program?"):
        print("Thank you for using Receipt Expanse Tracker!")
        window.destroy()
    else:
        pass

window = Tk()
window.title("Receipt Expanse Tracker")
window.geometry("600x650")
window.configure(bg="#ceecf5")

title1=Label(window,
            text=" Receipt Expanse Tracker",
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
                 bg="#90c9de",command=imp_dasgboard)#upload command later
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
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import validation

def open_edit_receipt_page(upload_page, receipt):

    app = tk.Toplevel(upload_page)
    app.title("Receipt Validation and Manual Edit")
    app.geometry("650x400")
    app.configure(bg="#ceecf5")

    def go_back():
        app.destroy()
        upload_page.deiconify()

    app.protocol("WM_DELETE_WINDOW", go_back)


    Label(
        app,
        text="Receipt Validation",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    main_frame = Frame(app)
    main_frame.pack(pady=10)

    # Merchant
    merchant_frame = Frame(main_frame)
    merchant_frame.grid(row=0, column=0, columnspan=3, sticky="w", pady=(5, 20))

    Label(merchant_frame, text="Merchant:", font=("Arial", 11)).pack(side=LEFT)

    merchant_entry = Entry(merchant_frame, width=40)
    merchant_entry.insert(0, receipt["merchant"])
    merchant_entry.pack(side=LEFT, padx=5)

    # Table headers
    Label(main_frame, text="Item Name", width=25, relief="solid").grid(row=2, column=0)
    Label(main_frame, text="Quantity", width=10, relief="solid").grid(row=2, column=1)
    Label(main_frame, text="Price (RM)", width=12, relief="solid").grid(row=2, column=2)

    item_rows = []

    for index, item in enumerate(receipt["items"]):

        name_entry = Entry(main_frame, width=25)
        name_entry.insert(0, item["name"])
        name_entry.grid(row=index + 3, column=0)

        qty_entry = Entry(main_frame, width=10, justify="center")
        qty_entry.insert(0, item["quantity"])
        qty_entry.grid(row=index + 3, column=1)

        price_entry = Entry(main_frame, width=12, justify="right")
        price_entry.insert(0, item["price"])
        price_entry.grid(row=index + 3, column=2)

        item_rows.append((name_entry, qty_entry, price_entry))

    # Total
    total_frame = Frame(main_frame)
    total_frame.grid(row=10, column=0, columnspan=3, sticky="w", pady=15)

    Label(total_frame, text="Total:", font=("Arial", 11)).pack(side=LEFT)

    total_entry = Entry(total_frame, width=12)
    total_entry.insert(0, receipt["total"])
    total_entry.pack(side=LEFT, padx=5)


    def save():

        receipt_data = {
            "merchant": merchant_entry.get(),
            "items": [],
            "total": total_entry.get()
        }

        for name, qty, price in item_rows:
            receipt_data["items"].append({
                "name": name.get(),
                "quantity": qty.get(),
                "price": price.get()
            })

        validation.save_receipt(receipt_data)

        messagebox.showinfo("Saved", "Receipt saved successfully!")

    # Save Button
    Button(app, text="Save", width=15, command=save).pack(pady=15)
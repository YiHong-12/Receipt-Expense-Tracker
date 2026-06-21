import tkinter as tk
from tkinter import *
from tkinter import messagebox
import validation
import categorize

def open_edit_receipt_page(upload_page, receipt):

    app = tk.Toplevel(upload_page)
    app.title("Receipt Validation and Manual Edit")
    app.minsize(700, 500)
    app.configure(bg="#ceecf5")

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

    Label(main_frame, text="Action", width=8, relief="solid").grid(row=2, column=3)

    item_rows = []
    next_row_idx = 3

    # Total Section
    total_frame = Frame(app, bg="#ceecf5")
    total_frame.pack(pady=10)
    Label(total_frame, text="Total:", font=("Arial", 11), bg="#ceecf5").pack(side=LEFT)

    total_entry = Entry(total_frame, width=12, state="readonly")
    total_entry.pack(side=LEFT, padx=5)

    # Automatic total calculation based on price column
    def calculate_total(*args):
        curr_total = 0.0
        for name_entry, qty_entry, price_entry in item_rows:
            try:
                # Only get price (ignores empty and text-filled variable)
                price_val = float(price_entry.get())
                curr_total += price_val
            except ValueError:
                pass
        
        total_entry.config(state="normal")
        total_entry.delete(0, tk.END)
        total_entry.insert(0, f"{curr_total:.2f}")
        total_entry.config(state="readonly")

    # function to add a new item row and delete existing rows
    def add_item_row(name="", qty="", price=""):
        nonlocal next_row_idx
        curr_row = next_row_idx
        next_row_idx += 1

        name_entry = Entry(main_frame, width=25)
        name_entry.insert(0, name)
        name_entry.grid(row=curr_row, column=0, pady=2)

        qty_entry = Entry(main_frame, width=10, justify="center")
        qty_entry.insert(0, qty)
        qty_entry.grid(row=curr_row, column=1, pady=2)

        price_entry = Entry(main_frame, width=12, justify="right")
        price_entry.insert(0, price)
        price_entry.grid(row=curr_row, column=2, pady=2)

        # Trigger calculate_total when price is entered
        price_entry.bind("<KeyRelease>", calculate_total)

        # function to delete a row
        def delete_row():
            name_entry.destroy()
            qty_entry.destroy()
            price_entry.destroy()
            delete_button.destroy()
            item_rows.remove((name_entry, qty_entry, price_entry))

            if row_data in item_rows:
                item_rows.remove(row_data)

            calculate_total()

        delete_button = Button(main_frame, text="❌", fg="red", command=delete_row)
        delete_button.grid(row=curr_row, column=3, padx=5, pady=2)

        row_data = (name_entry, qty_entry, price_entry)
        item_rows.append(row_data)

    # add initial item based on receipt
    for item in receipt.get("items", []):
        add_item_row(item["name"], item["quantity"], item["price"])

    # calculate initial total
    calculate_total()

    # button to add more items
    Button(app, text="+ Add New Item", width=15, command=add_item_row).pack(pady=5)

    # Save function
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

        items = []
        for name_entry, qty_entry, price_entry in item_rows:

            #convert quantity to numeric field
            try:
                qty = int(qty_entry.get())
            except ValueError:
                messagebox.showerror("Invalid Quantity",
                                 f"Quantity for '{name_entry.get()}' must be a number.")
                return

            #convert price tp numeric field
            try:
                price = float(price_entry.get())
            except ValueError:
                messagebox.showerror("Invalid Price",
                                 f"Price for '{name_entry.get()}' must be a number.")
                return
            
            items.append({
            "name": name_entry.get(),
            "quantity": qty,
            "price": price
            })

        #categorize the items
        items = categorize.categorize_transaction(items)

        #save the categorized items
        try:
            categorize.save_transaction(items, total_entry.get())
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save transaction: {e}")
            return

        messagebox.showinfo("Saved", "Receipt saved successfully!")

    # Save Button
    Button(app, text="Save", width=15, command=save).pack(pady=15)

    def go_back():
        app.destroy()
        upload_page.deiconify()

    app.protocol("WM_DELETE_WINDOW", go_back)
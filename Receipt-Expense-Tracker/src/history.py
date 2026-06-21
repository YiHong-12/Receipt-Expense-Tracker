from tkinter import ttk, Frame, Label, Button
import tkinter as tk
import json

OUTPUT_FILE = "edited_receipts.json"

# Treeview reference: https://www.pythontutorial.net/tkinter/tkinter-treeview/
def open_history_page(window):
    app = tk.Toplevel(window)
    app.title("Receipt History")
    app.minsize(700, 500)
    app.configure(bg="#ceecf5")

    Label(
        app,
        text="Receipt History",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    # Table frame
    table_frame = Frame(app, bg="#ceecf5")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Table columns
    columns = ("Date", "Merchant", "Total")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

    # Column Headings
    tree.heading("Date", text="Date & Time")
    tree.heading("Merchant", text="Merchant")
    tree.heading("Total", text="Total (RM)")

    tree.column("Date", width=150, anchor="center")
    tree.column("Merchant", width=180, anchor="w")
    tree.column("Total", width=90, anchor="e")

    # Row Styling
    style = ttk.Style()
    style.configure("Treeview", rowheight=25)
    tree.tag_configure("receipt", background="#d1e7dd") # Light green for the main receipt row
    tree.tag_configure("item", background="#ffffff")    # White for the item rows
    tree.tag_configure("space", background="#ceecf5")  # Matches window background to act as a visual gap

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    def open_receipt_details(event):
        # Guard if click on empty space
        selected = tree.selection()
        if not selected:
            return

        # Get item id when double clicked
        id = tree.selection()[0]
        values = tree.item(id, 'values')

        # Find receipt by matching the date
        for receipt in data:
            if receipt['date'] == values[0]:
                open_receipt_details_page(app, receipt)
                break

    tree.bind("<Double-1>", open_receipt_details)

    # Function to open receipt details page
    def open_receipt_details_page(window, receipt):
        detail_page = tk.Toplevel(window)
        detail_page.title("Saved Receipts History")
        detail_page.minsize(800, 450)  
        detail_page.configure(bg="#ceecf5")

        Label(
        detail_page,
        text="Receipt Details",
        font=("Arial", 16, "bold")
        ).pack(pady=15)
        
        cols = ("Item", "Quantity")
        item_tree = ttk.Treeview(detail_page, columns=cols, show="headings", height=10)
        item_tree.heading("Item", text="Item Name")
        item_tree.heading("Quantity", text="Quantity")
        item_tree.column("Item", width=250)
        item_tree.column("Quantity", width=100, anchor="center")
        item_tree.pack(padx=20, pady=10)

        for item in receipt.get("items", []):
            item_tree.insert("", "end", values=(item.get("name"), item.get("quantity")))

        Button(detail_page, text="Close", command=detail_page.destroy).pack(pady=10)


    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    if not data:
        Label(
        app,
        text="No Saved Receipt Found",
        font=("Arial", 12, "italic")
    ).pack(pady=15)
    
    else:
        for receipt in reversed(data):
            date = receipt.get("date", "N/A")
            merchant = receipt.get("merchant", "Unknown Merchant")
            total = receipt.get("total", "0.00")

            # Insert Data to date, merchant and total
            tree.insert("", "end", values=(date, merchant, total), tags=("receipt",)) 


    def go_back():
        app.destroy()
        window.deiconify()

    app.protocol("WM_DELETE_WINDOW", go_back)









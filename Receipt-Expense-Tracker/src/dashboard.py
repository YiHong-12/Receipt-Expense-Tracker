from tkinter import *
import tkinter as tk
from tkinter import ttk
from collections import defaultdict
import matplotlib.pyplot as plt
import categorize as db

def open_dashboard_page(window):
    app = tk.Toplevel(window)
    app.title("Receipt Expense Tracker - Dashboard")
    app.geometry("900x650")
    app.configure(bg="#ceecf5")

    title = Label(
        app,
        text="Expense Dashboard",
        font=("Ink Free", 30, "bold"),
        bg="#ceecf5",
        relief=RAISED,
        bd=15
    )
    title.pack(pady=10)

    def get_transactions():
        return db.load_transactions()


    def calculate_total_spending():
        return sum(float(t["total"]) for t in get_transactions())


    def calculate_filtered_total(category):
        if category == "All":
            return sum(float(t["total"]) for t in get_transactions())

        return sum(
            float(item["price"])
            for t in get_transactions()
            for item in t["items"]
            if item["category"] == category
        )


    def category_summary():
        summary = defaultdict(float)

        for t in get_transactions():
            for item in t["items"]:
                summary[item["category"]] += float(item["price"])

        return summary


    def merchant_summary():
        summary = defaultdict(float)

        for t in get_transactions():
            merchant = t.get("merchant", "Unknown")
            summary[merchant] += float(t["total"])

        return summary


    # CHARTS
    def show_category_chart():
        data = category_summary()

        plt.figure(figsize=(6, 6))
        plt.pie(data.values(), labels=data.keys(), autopct="%1.1f%%")
        plt.title("Expense by Category")
        plt.show()


    def show_merchant_chart():
        data = merchant_summary()

        plt.figure(figsize=(8, 5))
        plt.bar(data.keys(), data.values())
        plt.title("Spending by Merchant")
        plt.xlabel("Merchant")
        plt.ylabel("Amount (RM)")
        plt.tight_layout()
        plt.show()


    # CATEGORY LIST
    category_list = ["All"] + sorted({
        item.get("category", "others")
        for t in get_transactions()
        for item in t["items"]
    })


    # TABLE FUNCTIONS
    def populate_table(tree):
        for item in tree.get_children():
            tree.delete(item)

        for t in get_transactions():
            merchant = t.get("merchant", "Unknown")

            for item in t["items"]:
                tree.insert("", tk.END, values=(
                    t["date"],
                    merchant,
                    item.get("category", "others"),
                    f"RM {item['price']:.2f}"
                ))

    # FILTER FUNCTION
    def filter_transactions(tree, category):
        for item in tree.get_children():
            tree.delete(item)

        for t in get_transactions():
            merchant = t.get("merchant", "Unknown")

            for item in t["items"]:
                if category == "All" or item["category"] == category:
                    tree.insert("", END, values=(
                        t["date"],
                        merchant,
                        item["category"],
                        f"RM {item['price']:.2f}"
                    ))

        total = calculate_filtered_total(category)

        total_label.config(
            text=f"Total Spending ({category}): RM {total:.2f}"
        )
    


    def on_category_change(event):
        filter_transactions(tree, category_var.get())


    # Total label
    total_label = Label(
        app,
        text=f"Total Spending (All): RM {calculate_total_spending():.2f}",
        font=("Ink Free", 16, "bold"),
        bg="#ceecf5",
        fg="black"
    )
    total_label.pack(pady=10)


    # Chart buttons
    chart_frame = Frame(app, bg="#ceecf5")
    chart_frame.pack(pady=5)

    Button(
        chart_frame,
        text="Category Chart",
        width=18,
        height=2,
        font=("Ink Free", 13, "bold"),
        bg="#90c9de",
        command=show_category_chart
    ).pack(side=LEFT, padx=10)

    Button(
        chart_frame,
        text="Merchant Chart",
        width=18,
        height=2,
        font=("Ink Free", 13, "bold"),
        bg="#90c9de",
        command=show_merchant_chart
    ).pack(side=LEFT, padx=10)

    # Filter
    filter_frame = Frame(app, bg="#ceecf5")
    filter_frame.pack(pady=15)

    Label(filter_frame, 
          text="Filter Category:",
          font=("Ink Free", 13,"bold"),
          bg="#ceecf5"
          ).pack(side=LEFT)
       

    category_var = StringVar()
    category_var.set("All")

    category_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=category_var,
        values=category_list,
        state="readonly",
        width=18,
        font=("Arial", 11)
    )

    category_dropdown.pack(side=LEFT, padx=10)
    category_dropdown.bind("<<ComboboxSelected>>", on_category_change)


    # Table
    columns = ("Date", "Merchant", "Category", "Amount")

    tree = ttk.Treeview(
        app,
        columns=columns,
        show="headings",
        height=13
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180, anchor="center")

    tree.pack(fill=BOTH, expand=True, padx=30, pady=10)

    populate_table(tree)

    # Check whether the transaction file exists
    print("Loaded transactions:", get_transactions())

    def go_back():
        app.destroy()
        window.deiconify()

    app.protocol("WM_DELETE_WINDOW", go_back)

    back_button = Button(
        app,
        text="Back to Menu",
        width=20,
        height=2,
        font=("Ink Free", 13, "bold"),
        bg="#90c9de",
        command=go_back
    )
    back_button.pack(pady=10)
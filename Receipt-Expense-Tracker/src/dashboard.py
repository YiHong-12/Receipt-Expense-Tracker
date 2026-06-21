from tkinter import *
import tkinter as tk
from tkinter import ttk
from collections import defaultdict
import matplotlib.pyplot as plt
import categorize as db



def get_transactions():
    return db.load_transactions()

def calculate_total_spending():
    return sum(t["total"] for t in get_transactions())


def calculate_filtered_total(category):
    if category == "All":
        return sum(t["total"] for t in get_transactions())

    return sum(
        item["price"]
        for t in get_transactions()
        for item in t["items"]
        if item["category"] == category
    )


def category_summary():
    summary = defaultdict(float)

    for t in get_transactions():
        for item in t["items"]:
            summary[item["category"]] += item["price"]

    return summary


def merchant_summary():
    summary = defaultdict(float)

    for t in get_transactions():
        merchant = t.get("merchant", "Unknown")
        summary[merchant] += t["total"]

    return summary


# ==========================
# CHARTS
# ==========================
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


# ==========================
# CATEGORY LIST
# ==========================
category_list = ["All"] + sorted({
    item["category"]
    for t in get_transactions()
    for item in t["items"]
})


# ==========================
# TABLE FUNCTIONS
# ==========================
def populate_table(tree):
    for item in tree.get_children():
        tree.delete(item)

    for t in get_transactions():
        merchant = t.get("merchant", "Unknown")

        for item in t["items"]:
            tree.insert("", tk.END, values=(
                t["date"],
                merchant,
                item["category"],
                f"RM {item['price']:.2f}"
            ))


# ==========================
# FILTER FUNCTION
# ==========================
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


# ==========================
# GUI
# ==========================

def main():
    window = Tk()
    window.title("Receipt Expense Tracker - Dashboard")
    window.geometry("900x600")

    title = Label(
        window,
        text="Expense Dashboard",
        font=("Arial", 20, "bold")
    )
    title.pack(pady=10)

    # Total label
    total_label = Label(
        window,
        text=f"Total Spending (All): RM {calculate_total_spending():.2f}",
        font=("Arial", 14)
    )
    total_label.pack(pady=10)


    # Chart buttons
    chart_frame = Frame(window)
    chart_frame.pack()

    Button(
        chart_frame,
        text="Category Chart",
        command=show_category_chart
    ).pack(side=LEFT, padx=10)

    Button(
        chart_frame,
        text="Merchant Chart",
        command=show_merchant_chart
    ).pack(side=LEFT, padx=10)


    # Filter
    filter_frame = Frame(window)
    filter_frame.pack(pady=10)

    Label(filter_frame, text="Filter Category:").pack(side=LEFT)

    category_var = StringVar()
    category_var.set("All")

    category_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=category_var,
        values=category_list,
        state="readonly"
    )

    category_dropdown.pack(side=LEFT, padx=10)
    category_dropdown.bind("<<ComboboxSelected>>", on_category_change)


    # Table
    columns = ("Date", "Merchant", "Category", "Amount")

    tree = ttk.Treeview(
        window,
        columns=columns,
        show="headings",
        height=15
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180, anchor="center")

    tree.pack(fill=BOTH, expand=True)

    populate_table(tree)

    print("Loaded transactions:", get_transactions())

    window.mainloop()


if __name__ == "__main__":
    main()
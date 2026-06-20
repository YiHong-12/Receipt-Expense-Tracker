import sys
import tf_keras

# Redirect keras imports to tf_keras for compatibility
sys.modules['tensorflow.keras'] = tf_keras
sys.modules['keras'] = tf_keras

import keras_ocr
import math
import json
from pathlib import Path
from datetime import datetime

# Keywords used to match item names to categories
CATEGORY_KEYWORDS = {
    "food": ["bread", "milk", "egg", "rice", "chicken", "vegetable", "fruit", "snack", "drink"],
    "transport": ["grab", "taxi", "petrol", "fuel", "parking", "toll"],
    "household": ["detergent", "tissue", "soap", "shampoo"],
    "electronics": ["cable", "charger", "battery", "phone"],
}

# File path where transactions will be saved
DATA_FILE = "transactions.txt"


def categorize_item(item_name):
    # Convert to lowercase so it is not case-sensitive
    item_name = item_name.lower()

    # Loop through each category and its keywords
    for category in CATEGORY_KEYWORDS:
        keywords = CATEGORY_KEYWORDS[category]
        for keyword in keywords:
            # If keyword is found anywhere in the item name, return that category
            if keyword in item_name:
                return category

    # If no keyword matched, return "others" as the default category
    return "others"


def categorize_transaction(items):
    # Add a "category" key to each item based on its name
    for item in items:
        item["category"] = categorize_item(item["name"])
    return items


def summarize_by_category(items):
    # Build a dictionary that totals the price spent per category
    summary = {}
    for item in items:
        cat = item["category"]
        if cat in summary:
            # Category already exists, add to the running total
            summary[cat] += item["price"]
        else:
            # First time seeing this category, create a new entry
            summary[cat] = item["price"]
    return summary


def load_transactions():
    # If the file does not exist yet, return an empty list
    if not Path(DATA_FILE).exists():
        return []

    # Open and read the existing transaction data from the file
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_transaction(items, total):
    # Load existing transactions so we don't overwrite them
    transactions = load_transactions()

    # Add the new transaction as a dictionary with date, items, and total
    transactions.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": items,
        "total": total
    })

    # Write the updated list back to the file
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=4)

    print("Transaction saved successfully!")


if __name__ == "__main__":
    # Load all previously saved transactions from the file
    transactions = load_transactions()

    if not transactions:
        print("No saved transactions found.")
    else:
        # Loop through each saved transaction and display its details
        for transaction in transactions:
            items = categorize_transaction(transaction["items"])
            summary = summarize_by_category(items)

            print(f"Date: {transaction['date']}")

            # Print each item with its price and assigned category
            for item in items:
                print(f"{item['name']} - RM{item['price']} - {item['category']}")

            print("Summary:", summary)
            print()
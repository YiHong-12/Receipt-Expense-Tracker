import json
from datetime import datetime

OUTPUT_FILE = "edited_receipts.json"

def save_receipt(receipt_data):

    receipt_data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # load existing data
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(receipt_data)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return True
import re
import text_extractor

def parse_receipt(rows):
    result = {
        "merchant": "",
        "items": [],
        "total": None
    }

    total_keywords = ["total", "grand total", "amount due", "net payable", "total due", "bal due"]
    ignore_keywords = ["subtotal", "sub total", "tax", "vat", "gst", "change", "cash", "visa", "mastercard", "amex", "tendered"]

    for row in rows:
        texts = [t["text"] for t in row["data"]]
        raw_line = " ".join(texts).strip()

        line =  re.sub(r'(\d+)\s*\.\s*(\d{2})', r'\1.\2', raw_line).lower()

        if not line:
            continue

        # 1. TOTAL detection
        if any(k in line for k in total_keywords) and not any(k in line for k in ignore_keywords):
            numbers = re.findall(r"\d+\.\d{2}", line)
            if numbers:
                result["total"] = float(numbers[-1])
            continue

        # 2. MERCHANT detection (first non-numeric meaningful line)
        if result["merchant"] == "":
            if not any(re.search(r"\d", t) for t in texts):
                result["merchant"] = " ".join(texts)
                continue
        
        # 3. ITEM detection
        if any(k in line for k in ignore_keywords) or any(k in line for k in total_keywords):
            continue

        price = re.findall(r"\d+\.\d{2}", line)
        if not price:
            continue

        item_price = float(price[-1])

        name_and_quantity = line
        for p in price:
            name_and_quantity = name_and_quantity.replace(p, "",1)

        name_and_quantity = re.sub(r'[\$\€\£\*\:\-]', '', name_and_quantity).strip()

        qty = 1
        quantity_match = re.search(r'^\b(\d+)\b|\b(\d+)\b$', name_and_quantity)
        if quantity_match:
            quantity_str = quantity_match.group(1) or quantity_match.group(2)
            if int(quantity_str) < 100:
                qty = int(quantity_str)
                name_and_quantity = name_and_quantity.replace(quantity_str, "", 1)

        name = re.sub(r'\s+', ' ', name_and_quantity).strip()

        if name:
            result["items"].append({
                "name": name,
                "quantity": qty,
                "price": price
            })

    return result

parsed_receipt = parse_receipt(extracted_text)
print(parsed_receipt)

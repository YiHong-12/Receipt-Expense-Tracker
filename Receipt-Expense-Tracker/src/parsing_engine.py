import re
import os
import text_extractor

from matplotlib import image, text

def parse_receipt(raw_texts):
    # Extract possible price tokens
    price_indices = []
    for i, w in enumerate(raw_texts):
        if re.fullmatch(r'[sS]?\d{3,6}', w):
            price_indices.append(i)

    if not price_indices:
        return {
            "merchant": "",
            "items": [],
            "total": None
        }
    
    #Group texts into lines
    lines = []
    start = 0
    for i in price_indices:
        # include price token at the end of the line
        line = raw_texts[start:i+1]
        lines.append(" ".join(line))
        start = i+1

    # remaining texts after last price token
    if start < len(raw_texts):
        lines.append(" ".join(raw_texts[start:]))
     
    # Data parsing
    result = {
        "merchant": "",
        "items": [],
        "total": None
    }

    total_keywords = ["total", "grand total", "amount due", "net payable", "total due", "bal due"]
    ignore_keywords = ["subtotal", "sub total", "tax", "vat", "gst", "change", "cash", "visa", "mastercard", "amex", "tendered"]

    for line in lines:
        line_lc = line.lower().strip()
        if not line_lc:
            continue

        # Detect total amount
        if any(text in line_lc for text in total_keywords) and not any(text in line_lc for text in ignore_keywords):
            #find any possible price token at the end 
            numbers = re.findall(r'[sS]?\d{3,6}', line_lc)
            if numbers:
                #fix common OCR errors
                raw = numbers[-1].lower().replace('s','').replace('o','0')

                if raw.isdigit() and len(raw) >= 2:
                    result["total"] = float(raw[:-2] + "." + raw[-2:])
            continue
            

        # Detect merchant name
        if result["merchant"] == "" and not re.search(r'\d', line_lc):
            result["merchant"] = line
            continue
        
        # Detect items (must contain price token at the end)
        if any(text in line for text in ignore_keywords) or any(text in line for text in total_keywords):
            continue
        
        price_match = re.search(r'([sS]?\d{3,6})\s*$', line_lc)
        if not price_match:
            continue

        price_token = price_match.group(1).lower().replace('s','').replace('o','0') #fix common OCR errors
        if not price_token.isdigit() or len(price_token) < 2:
            continue
        price = float(price_token[:-2] + "." + price_token[-2:])
    
        # Item name (everything before the price token)
        item_name = line_lc[:price_match.end()].strip()

        # Quantity (leading number)
        qty = 1
        qty_match = re.match(r'(\d+)\s+', item_name)
        if qty_match:
            qty_val = int(qty_match.group(1))
            if qty_val < 100:           # quantity threshold to avoid misinterpretation of prices as quantities
                qty = qty_val
                item_name = item_name[qty_match.end():].strip()

        # Final cleaning
        name = re.sub(r'[\$\€\£\*\-]', '', item_name).strip()
        name = re.sub(r'\s+', ' ', name)
        if name:
            result["items"].append({"name": name, "quantity": qty, "price": price})

    return result

def upload_and_parse_receipt(image_path):
    extracted_text = ['artisans', 'the', 'pantry', 'foods', 'fine', 'market', '789', 'willow', 'rd', 'tx', '78701', '5550199', 'creek', 'austin', '101', '512', 'cash', 'receipt', 'qty', 'item', 'amount', 'sourdough', 'loaf', '5650', '1', 'wildflower', 's1499', 'honey', 'jar', 'l', 's825', 'pantry', 'artisan', 'crackers', '1', 'coffee', 's1850', 'bag', 'fairtrade', '1', 'kombucha', 'bottles', '51000', '2', 'cheddar', 'wedge', 'smoked', '510', '18', '1', 's6842', 'total', 'sto00', 'cash', 'change', '5158', 'for', 'with', 'custom', 'sincere', 'appreciation', 'your', 'the', 'artisans', 'pantry', 'ap']
    parsed_receipt = parse_receipt(extracted_text)
    return parsed_receipt

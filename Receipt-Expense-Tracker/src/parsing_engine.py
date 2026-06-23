import re
import os
import text_extractor


# Fix OCR character mistakes when the text is very likely a number 
OCR_DIGIT_MAP = str.maketrans({
    'O': '0', 'o': '0',
    'I': '1', 'l': '1', 'i': '1',
    'Z': '2', 'z': '2',
    'B': '8',
    'G': '6', 'g': '6',
    'T': '7',
})

# Possible phrases that indicate the final total on a receipt
TOTAL_KEYWORDS = frozenset([
    "total", "grand total", "amount due", "net payable",
    "total due", "bal due", "balance due", "amt due",
])

# Phrases that disqualify a line from being a grand-total line
SUBTOTAL_KEYWORDS = frozenset([
    "subtotal", "sub total", "sub-total",
    "tax", "vat", "gst", "hst", "pst",
    "change", "cash", "visa", "mastercard", "amex",
    "tendered", "tip", "gratuity", "discount",
])

# Keywords that mark a line as metadata
META_KEYWORDS = frozenset([
    # address
    "street", "road", " rd", " st", "avenue", "blvd", "lane", "country",
    # contact
    "tel", "phone", "fax", "email", "website", "www.",
    # receipt header boilerplate
    "date", "time", "receipt", "invoice", "cashier", "register",
    "trans", "transaction",
    # column headers
    "qty", "item", "description", "amount", "price", "unit",
    # payment lines
    "auth", "debit", "payment",
    # loyalty / policy
    "conditions", "policy", "member", "loyalty",
    # item-count summary
    "items sold", "no. of items", "no of items",
    # closing / footer phrases  
    "welcome", "thank", "visit", "sincere", "appreciation",
    "custom", "enjoy", "please", "come again",
    # store type words that appear in footers / merchant banners
    "fine foods", "market", "store", "supermarket", "grocery",
])

# Patterns that look like receipt metadata even without keywords
# date/time/ID lines
_RE_PURELY_NUMERIC = re.compile(r'^\s*[\d\s\-/:]+\s*$')  
_RE_PHONE = re.compile(r'(\+?\d[\d\s\-().]{6,}\d)')


def group_words_into_lines(words, y_threshold_ratio=0.7):

    # Cluster OCR word-boxes into text lines by y-centre proximity
    if not words:
        return []

    processed = []
    for item in words:
        y_center = (item["y_min"] + item["y_max"]) / 2.0
        height = item["y_max"] - item["y_min"]
        processed.append({
            "word": item["word"],
            "y_center": y_center,
            "height": max(height, 1.0),
            "x_min": item["x_min"],
            "x_max": item["x_max"],
        })

    processed.sort(key=lambda x: x["y_center"])

    lines = []
    current_line = []
    for item in processed:
        if not current_line:
            current_line.append(item)
        else:
            anchor = current_line[0]
            threshold = anchor["height"] * y_threshold_ratio
            if abs(item["y_center"] - anchor["y_center"]) <= threshold:
                current_line.append(item)
            else:
                lines.append(current_line)
                current_line = [item]

    if current_line:
        lines.append(current_line)

    return [sorted(line, key=lambda x: x["x_min"]) for line in lines]


def merge_adjacent_words(line_words, threshold=2.0):

    # Merge word-boxes that were split by the OCR engine but belong together
    if not line_words:
        return []

    merged = []
    current = line_words[0].copy()

    for next_word in line_words[1:]:
        gap = next_word["x_min"] - current["x_max"]
        if gap < threshold:
            current["word"] = current["word"] + next_word["word"]
            current["x_max"] = next_word["x_max"]
        else:
            merged.append(current)
            current = next_word.copy()

    merged.append(current)
    return merged



# Price parsing
_RE_LEADING_CURRENCY = re.compile(
    r'^[5S$€£¥₹](?=[\d(Oo0IilZzBbGgT])',
)
_RE_PAREN_NEGATIVE = re.compile(r'^\(([^)]+)\)$')
_RE_STRAY_PARENS = re.compile(r'[()]')
_RE_DASHES = re.compile(r'[–—]')


def _token_has_price_structure(token: str) -> bool:
   
    # Determine whether a token looks like a price before OCR correction.
    raw = token.strip()
    if not raw:
        return False

    # Strip known currency prefix for the digit-ratio test
    core = re.sub(r'^[$€£¥₹5S]', '', raw)   

    # Rule 1: explicit decimal
    if '.' in core:
        return True

    # Rule 2: leading real currency symbol (not 5/S since those need rule 1)
    if raw and raw[0] in '$€£¥₹':
        return True

    # Rule 3: more real digits than letters in the original token
    digit_count = sum(c.isdigit() for c in raw)
    alpha_count = sum(c.isalpha() for c in raw)
    return digit_count > alpha_count and digit_count >= 2


def _pre_clean_price_token(token: str):

    # Apply symbol-level corrections before digit substitution
    is_negative = False

    token = _RE_DASHES.sub('-', token)

    m = _RE_PAREN_NEGATIVE.match(token)
    if m:
        token = m.group(1)
        is_negative = True
    else:
        token = _RE_STRAY_PARENS.sub('', token)

    token = _RE_LEADING_CURRENCY.sub('', token)

    return token, is_negative


def _apply_ocr_digit_corrections(token: str) -> str:

    token = re.sub(r'[\s$€£¥₹,]', '', token)
    if re.fullmatch(r'\d+\.\d{1,2}', token):
        return token
   
    return token.translate(OCR_DIGIT_MAP)


def parse_price_value(token: str):

    # Return a float price from a raw OCR token
    if not token:
        return None

    has_digit = any(c.isdigit() for c in token)
    has_correctable = any(c in 'OoIilZzBbGgT' for c in token)
    if not has_digit and not has_correctable:
        return None

    # Reject tokens that are clearly text words, even if they happen to contain letters that are in OCR_DIGIT_MAP (o, i, l, b, g, t, z)
    if not _token_has_price_structure(token):
        return None

    # Symbol-level pre-cleaning 
    token, is_negative = _pre_clean_price_token(token)

    if not token or not any(c.isdigit() or c in 'OoIilZzBbGgT' for c in token):
        return None

    # OCR digit corrections 
    cleaned = _apply_ocr_digit_corrections(token)
    cleaned = re.sub(r'[^\d.]', '', cleaned)

    if not cleaned:
        return None

    # Explicit decimal match 
    decimal_match = re.search(r'\d+\.\d{1,2}', cleaned)
    if decimal_match:
        value = float(decimal_match.group(0))
        if is_negative:
            value = -value
        if 0.01 <= abs(value) <= 9999.99:
            return value
        return None

    # Fallback – last two digits as cents 
    digits = re.sub(r'\D', '', cleaned)
    if len(digits) < 2:
        return None

    value = float(digits[:-2] + '.' + digits[-2:])
    if is_negative:
        value = -value
    if 0.01 <= abs(value) <= 9999.99:
        return value
    return None



# Merchant extraction
def _is_meta_line(line_str: str) -> bool:

    # Return True when a line looks like address/contact/header metadata
    lc = line_str.lower()

    if any(kw in lc for kw in META_KEYWORDS):
        return True

    digit_ratio = sum(c.isdigit() for c in line_str) / max(len(line_str), 1)
    if digit_ratio > 0.5:
        return True

    if _RE_PHONE.search(line_str):
        return True

    return False


def extract_merchant(lines):

    # Infer the merchant name from the top portion of the receipt
    candidates = []

    for line in lines[:8]:
        line_str = " ".join(w["word"] for w in line).strip()

        if not line_str:
            continue
        if _is_meta_line(line_str):
            continue
        if parse_price_value(line_str) is not None and len(line_str) < 10:
            continue

        words = [
            w for w in line_str.split()
            if len(w) > 1 or w.lower() in ('a', '&')
        ]
        if not words:
            continue

        clean = " ".join(words).strip()
        if clean:
            candidates.append(clean)

    if not candidates:
        return "Unknown"

    merchant = candidates[0]
    if len(candidates) > 1 and len(merchant.split()) <= 2:
        second = candidates[1]
        if not _is_meta_line(second) and len(second.split()) <= 5:
            merchant = merchant + " " + second

    return re.sub(r'\s+', ' ', merchant).strip()



# Line classification
def _is_total_line(line_lc: str) -> bool:
    return (
        any(kw in line_lc for kw in TOTAL_KEYWORDS)
        and not any(kw in line_lc for kw in SUBTOTAL_KEYWORDS)
    )


def _is_ignorable_line(line_lc: str) -> bool:
    return (
        any(kw in line_lc for kw in SUBTOTAL_KEYWORDS)
        or any(kw in line_lc for kw in META_KEYWORDS)
        or _RE_PURELY_NUMERIC.match(line_lc) is not None
    )



# Quantity detection
_RE_QTY_PREFIX = re.compile(r'^(\d{1,3})[xX]$')
_RE_STANDALONE_INT = re.compile(r'^\d{1,3}$')


def _extract_qty_from_words(item_words):

    # Detect a leading quantity token (e.g. '2x', '2X', or a bare small integer)
    if not item_words:
        return 1, item_words

    first = item_words[0]["word"]

    m = _RE_QTY_PREFIX.match(first)
    if m:
        return int(m.group(1)), item_words[1:]

    if _RE_STANDALONE_INT.match(first):
        qty = int(first)
        if qty < 100:
            return qty, item_words[1:]

    # Some OCRs output lowercase 'l' for '1'
    if first.lower() == 'l' and len(item_words) > 1:
        return 1, item_words[1:]

    return 1, item_words


# Item name cleanup
_RE_NOISE = re.compile(r'[$€£*#@]+')
_RE_MULTI_SPACE = re.compile(r'\s{2,}')


def clean_item_name(raw: str) -> str:

    # Generic cleanup for an item name string from a receipt line
    name = _RE_NOISE.sub('', raw)
    name = _RE_MULTI_SPACE.sub(' ', name).strip()
    # Title-case only when the string is fully upper or fully lower
    if name == name.upper() or name == name.lower():
        name = name.title()
    return name



# Item-name word filter
_ITEM_NAME_REJECT_WORDS = frozenset([
    "qty", "item", "amount", "price", "total", "subtotal",
    "cash", "change", "tax", "vat", "gst",
    "sincere", "appreciation", "welcome", "thank", "visit",
    "enjoy", "custom", "please",
])


def _item_name_is_valid(name: str) -> bool:
    
    # Return False if the assembled item name looks like a receipt header, footer, or payment line rather than a real product name
    if len(name.replace(' ', '')) < 2:
        return False
    lc = name.lower()
    # Reject if any structural keyword dominates the name
    words = lc.split()
    reject_count = sum(1 for w in words if w in _ITEM_NAME_REJECT_WORDS)
    if reject_count > 0 and reject_count >= len(words) / 2:
        return False
    return True


def parse_receipt(raw_text_data):
   
    if not raw_text_data:
        return {"merchant": "", "items": [], "total": None}

    if isinstance(raw_text_data[0], str):
        raw_text_data = [
            {
                "word": word,
                "y_min": float(i * 10),
                "y_max": float(i * 10 + 8),
                "x_min": 0.0,
                "x_max": 10.0,
            }
            for i, word in enumerate(raw_text_data)
        ]

    lines = group_words_into_lines(raw_text_data)
    merged_lines = [merge_adjacent_words(line) for line in lines]

    merchant = extract_merchant(merged_lines)

    items = []
    total_candidates = []

    for line in merged_lines:
        line_str = " ".join(w["word"] for w in line).strip()
        line_lc = line_str.lower()

        # Total line 
        if _is_total_line(line_lc):
            price_vals = [
                parse_price_value(w["word"])
                for w in line
                if parse_price_value(w["word"]) is not None
            ]
            if price_vals:
                total_candidates.append(max(price_vals))
            continue

        # Metadata / ignorable line
        if _is_ignorable_line(line_lc):
            continue

        # Find the rightmost valid price on this line 
        price_val = None
        price_word_idx = -1

        for i in range(len(line) - 1, -1, -1):
            val = parse_price_value(line[i]["word"])
            if val is not None:
                price_val = val
                price_word_idx = i
                break

        if price_val is None or price_word_idx == -1:
            continue

        # All words to the LEFT of the price are the item description
        item_words = line[:price_word_idx]
        if not item_words:
            continue

        # If the word immediately before the price is ALSO a valid price
        # (unit-price column followed by line-total column), drop it.
        # Guard: only drop if it genuinely parses as a price AND is not a word
        # that could be part of the item name.
        if len(item_words) >= 1:
            prev_word = item_words[-1]["word"]
            prev_val = parse_price_value(prev_word)
            # Only discard if it really is a numeric/price token, not a text word
            if prev_val is not None and _token_has_price_structure(prev_word):
                item_words = item_words[:-1]

        if not item_words:
            continue

        # Extract leading quantity token
        qty, item_words = _extract_qty_from_words(item_words)

        if not item_words:
            continue

        raw_name = " ".join(w["word"] for w in item_words)
        item_name = clean_item_name(raw_name)

        if not _item_name_is_valid(item_name):
            continue

        items.append({
            "name": item_name,
            "quantity": qty,
            "price": price_val,
        })

    # Resolve total
    if total_candidates:
        total = max(total_candidates)
    else:
        calculated = sum(it["price"] for it in items)
        total = round(calculated, 2) if calculated > 0 else None

    return {
        "merchant": merchant,
        "items": items,
        "total": float(total) if total is not None else None,
    }


def upload_and_parse_receipt(image_path):
    extracted_text = text_extractor.extract_raw_text(image_path)
    return parse_receipt(extracted_text)
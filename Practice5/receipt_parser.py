
import re
import json
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding="utf-8")

# Read receipt text from raw.txt
file_path = Path(__file__).parent / "raw.txt"
text = file_path.read_text(encoding="utf-8")


# Convert Kazakhstani price format to a number
# Example: "1 200,00" -> 1200.00
def parse_price(value):
    value = value.replace(" ", "")
    value = value.replace(",", ".")
    return float(value)


# 1. Extract all prices
price_pattern = r"(?<!\d)(?:\d{1,3}(?: \d{3})*|\d+),\d{2}(?!\d)"
all_prices = re.findall(price_pattern, text)

prices = [parse_price(price) for price in all_prices]


# 2. Extract product names, quantities and prices
products = []

# Split receipt into blocks by product numbers
blocks = re.split(r"(?m)^\s*(\d+)\.\s*$", text)

for i in range(1, len(blocks), 2):
    number = int(blocks[i])
    block = blocks[i + 1]

    # Stop if the product section has ended
    if re.search(r"Банковская карта|ИТОГО", block):
        block = re.split(
            r"Банковская карта|ИТОГО", block
        )[0]

    # Extract quantity and unit price
    match = re.search(
        r"([0-9]+,[0-9]+)\s*x\s*"
        r"([0-9 ]+,[0-9]{2})",
        block
    )

    if not match:
        continue

    quantity = float(match.group(1).replace(",", "."))
    unit_price = parse_price(match.group(2))

    # Product name appears before the quantity line
    name = block[:match.start()].strip()
    name = re.sub(r"\s+", " ", name)

    # Find the item total after the quantity line
    remaining = block[match.end():]

    total_match = re.search(
        r"(?m)^\s*([0-9 ]+,[0-9]{2})\s*$",
        remaining
    )

    if total_match:
        total_price = parse_price(total_match.group(1))
    else:
        total_price = round(quantity * unit_price, 2)

    products.append({
        "number": number,
        "name": name,
        "quantity": int(quantity) if quantity.is_integer() else quantity,
        "unit_price": unit_price,
        "total_price": total_price
    })


# 3. Calculate total from product prices
calculated_total = round(
    sum(product["total_price"] for product in products), 2
)


# 4. Extract date and time
datetime_match = re.search(
    r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+"
    r"(\d{2}:\d{2}:\d{2})",
    text
)

date = datetime_match.group(1) if datetime_match else None
time = datetime_match.group(2) if datetime_match else None


# 5. Extract payment method
payment_match = re.search(
    r"Банковская карта:\s*([0-9 ]+,[0-9]{2})",
    text
)

payment_method = (
    "Банковская карта" if payment_match else None
)

payment_amount = (
    parse_price(payment_match.group(1))
    if payment_match else None
)


# 6. Extract receipt total
total_match = re.search(
    r"ИТОГО:\s*([0-9 ]+,[0-9]{2})",
    text
)

receipt_total = (
    parse_price(total_match.group(1))
    if total_match else None
)


# Extract receipt number
receipt_number_match = re.search(
    r"Чек №(\d+)",
    text
)

receipt_number = (
    receipt_number_match.group(1)
    if receipt_number_match else None
)


# Create structured JSON output
result = {
    "store": "EUROPHARMA",
    "receipt_number": receipt_number,
    "prices": all_prices,
    "products": products,
    "product_count": len(products),
    "calculated_total": calculated_total,
    "receipt_total": receipt_total,
    "date": date,
    "time": time,
    "payment_method": payment_method,
    "payment_amount": payment_amount
}


# Print result
print(json.dumps(result, indent=4, ensure_ascii=False))
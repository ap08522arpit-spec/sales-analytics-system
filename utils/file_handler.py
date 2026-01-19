def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw lines (strings)
    """
    encodings = ["utf-8", "latin-1", "cp1252"]

    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc) as file:
                lines = file.readlines()

            cleaned_lines = []
            for line in lines[1:]:
                line = line.strip()
                if line:
                    cleaned_lines.append(line)

            return cleaned_lines

        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print("File not found:", filename)
            return []

    print("Could not read file due to encoding issues.")
    return []

#Task 1.2

def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """
    transactions = []

    for line in raw_lines:
        fields = line.split("|")

        if len(fields) != 8:
            continue

        txn_id, date, prod_id, prod_name, qty, price, cust_id, region = fields

        prod_name = prod_name.replace(",", "")

        try:
            qty = int(qty.replace(",", ""))
            price = float(price.replace(",", ""))
        except ValueError:
            continue

        transactions.append({
            "TransactionID": txn_id,
            "Date": date,
            "ProductID": prod_id,
            "ProductName": prod_name,
            "Quantity": qty,
            "UnitPrice": price,
            "CustomerID": cust_id,
            "Region": region
        })

    return transactions

# Task 1.3
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid = []
    invalid_count = 0

    for tx in transactions:
        if (
            tx["Quantity"] <= 0 or
            tx["UnitPrice"] <= 0 or
            not tx["TransactionID"].startswith("T") or
            not tx["ProductID"].startswith("P") or
            not tx["CustomerID"].startswith("C")
        ):
            invalid_count += 1
            continue

        valid.append(tx)

    if region:
        valid = [t for t in valid if t["Region"] == region]

    if min_amount or max_amount:
        filtered = []
        for t in valid:
            amount = t["Quantity"] * t["UnitPrice"]
            if (min_amount is None or amount >= min_amount) and \
               (max_amount is None or amount <= max_amount):
                filtered.append(t)
        valid = filtered

    summary = {
        "total_input": len(transactions),
        "invalid": invalid_count,
        "final_count": len(valid)
    }

    return valid, invalid_count, summary


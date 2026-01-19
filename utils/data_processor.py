from datetime import datetime
from collections import defaultdict


def clean_and_validate_data(lines):
    total_records = 0
    invalid_records = 0
    valid_records = []

    for line in lines[1:]:  # skip header
        total_records += 1
        fields = line.split("|")

        if len(fields) != 8:
            invalid_records += 1
            continue

        txn_id, date, prod_id, prod_name, qty, price, cust_id, region = fields

        # Validate Transaction ID
        if not txn_id.startswith("T"):
            invalid_records += 1
            continue

        # Validate CustomerID and Region
        if not cust_id or not region:
            invalid_records += 1
            continue

        # Clean numeric values
        try:
            qty = int(qty.replace(",", ""))
            price = float(price.replace(",", ""))
        except ValueError:
            invalid_records += 1
            continue

        # Validate numeric rules
        if qty <= 0 or price <= 0:
            invalid_records += 1
            continue

        # Clean product name
        prod_name = prod_name.replace(",", "")

        valid_records.append({
            "TransactionID": txn_id,
            "Date": date,
            "ProductID": prod_id,
            "ProductName": prod_name,
            "Quantity": qty,
            "UnitPrice": price,
            "CustomerID": cust_id,
            "Region": region
        })

    return total_records, invalid_records, valid_records



#Task 2.1 (a)
def calculate_total_revenue(transactions):
    total_revenue = 0.0

    for tx in transactions:
        total_revenue += tx["Quantity"] * tx["UnitPrice"]

    return total_revenue

#Task 2.1 (b)
def region_wise_sales(transactions):
    region_data = {}
    total_revenue = calculate_total_revenue(transactions)

    for tx in transactions:
        region = tx["Region"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += amount
        region_data[region]["transaction_count"] += 1

    for region in region_data:
        region_data[region]["percentage"] = round(
            (region_data[region]["total_sales"] / total_revenue) * 100, 2
        )

    # Sort by total_sales descending
    region_data = dict(
        sorted(
            region_data.items(),
            key=lambda x: x[1]["total_sales"],
            reverse=True
        )
    )

    return region_data

# Task 2.1 (c)
def customer_analysis(transactions):
    customers = {}

    for tx in transactions:
        cid = tx["CustomerID"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        product = tx["ProductName"]

        if cid not in customers:
            customers[cid] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customers[cid]["total_spent"] += amount
        customers[cid]["purchase_count"] += 1
        customers[cid]["products_bought"].add(product)

    for cid in customers:
        customers[cid]["avg_order_value"] = round(
            customers[cid]["total_spent"] / customers[cid]["purchase_count"], 2
        )
        customers[cid]["products_bought"] = list(customers[cid]["products_bought"])

    customers = dict(
        sorted(
            customers.items(),
            key=lambda x: x[1]["total_spent"],
            reverse=True
        )
    )

    return customers

#Task 2.1 (d)
def customer_analysis(transactions):
    customers = {}

    for tx in transactions:
        cid = tx["CustomerID"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        product = tx["ProductName"]

        if cid not in customers:
            customers[cid] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customers[cid]["total_spent"] += amount
        customers[cid]["purchase_count"] += 1
        customers[cid]["products_bought"].add(product)

    for cid in customers:
        customers[cid]["avg_order_value"] = round(
            customers[cid]["total_spent"] / customers[cid]["purchase_count"], 2
        )
        customers[cid]["products_bought"] = list(customers[cid]["products_bought"])

    customers = dict(
        sorted(
            customers.items(),
            key=lambda x: x[1]["total_spent"],
            reverse=True
        )
    )

    return customers

#Task 2.2 (a) Daily Sales Trend
def daily_sales_trend(transactions):
    daily = {}

    for tx in transactions:
        date = tx["Date"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if date not in daily:
            daily[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "unique_customers": set()
            }

        daily[date]["revenue"] += amount
        daily[date]["transaction_count"] += 1
        daily[date]["unique_customers"].add(tx["CustomerID"])

    for date in daily:
        daily[date]["unique_customers"] = len(daily[date]["unique_customers"])

    return dict(sorted(daily.items()))

# Task 2.2 (b) Peak Sales Day
def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)

    peak_date = max(
        daily.items(),
        key=lambda x: x[1]["revenue"]
    )

    return (
        peak_date[0],
        peak_date[1]["revenue"],
        peak_date[1]["transaction_count"]
    )

#Task 2.3 Low Performing Products

def low_performing_products(transactions, threshold=10):
    products = {}

    for tx in transactions:
        name = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]

        if name not in products:
            products[name] = {"qty": 0, "revenue": 0.0}

        products[name]["qty"] += qty
        products[name]["revenue"] += revenue

    result = [
        (name, data["qty"], data["revenue"])
        for name, data in products.items()
        if data["qty"] < threshold
    ]

    result.sort(key=lambda x: x[1])

    return result

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    with open(output_file, 'w', encoding='utf-8') as file:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        file.write("=" * 50 + "\n")
        file.write("           SALES ANALYTICS REPORT\n")
        file.write(f"Generated: {now}\n")
        file.write(f"Records Processed: {len(transactions)}\n")
        file.write("=" * 50 + "\n\n")
        total_revenue = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
        avg_order = total_revenue / len(transactions)
        dates = [t['Date'] for t in transactions]

        file.write("OVERALL SUMMARY\n")
        file.write("-" * 45 + "\n")
        file.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        file.write(f"Total Transactions:   {len(transactions)}\n")
        file.write(f"Average Order Value:  ₹{avg_order:,.2f}\n")
        file.write(f"Date Range:           {min(dates)} to {max(dates)}\n\n")
        region_data = defaultdict(lambda: {'sales': 0, 'count': 0})

        for t in transactions:
            amount = t['Quantity'] * t['UnitPrice']
            region_data[t['Region']]['sales'] += amount
            region_data[t['Region']]['count'] += 1

        file.write("REGION-WISE PERFORMANCE\n")
        file.write("-" * 45 + "\n")
        file.write(f"{'Region':10} {'Sales':12} {'% of Total':12} {'Transactions'}\n")

        for region, data in sorted(region_data.items(), key=lambda x: x[1]['sales'], reverse=True):
            percent = (data['sales'] / total_revenue) * 100
            file.write(f"{region:10} ₹{data['sales']:10,.0f} {percent:10.2f}% {data['count']:10}\n")

        file.write("\n")
        product_summary = defaultdict(lambda: {'qty': 0, 'rev': 0})

        for t in transactions:
            product_summary[t['ProductName']]['qty'] += t['Quantity']
            product_summary[t['ProductName']]['rev'] += t['Quantity'] * t['UnitPrice']

        file.write("TOP 5 PRODUCTS\n")
        file.write("-" * 45 + "\n")
        file.write("Rank  Product        Quantity  Revenue\n")

        for i, (product, data) in enumerate(
            sorted(product_summary.items(), key=lambda x: x[1]['qty'], reverse=True)[:5], 1):
            file.write(f"{i:<5} {product:14} {data['qty']:8} ₹{data['rev']:,.0f}\n")

        file.write("\n")
        customer_summary = defaultdict(lambda: {'spent': 0, 'count': 0})

        for t in transactions:
            amt = t['Quantity'] * t['UnitPrice']
            customer_summary[t['CustomerID']]['spent'] += amt
            customer_summary[t['CustomerID']]['count'] += 1

        file.write("TOP 5 CUSTOMERS\n")
        file.write("-" * 45 + "\n")
        file.write("Rank  CustomerID  Total Spent  Orders\n")

        for i, (cid, data) in enumerate(
            sorted(customer_summary.items(), key=lambda x: x[1]['spent'], reverse=True)[:5], 1):
            file.write(f"{i:<5} {cid:10} ₹{data['spent']:10,.0f} {data['count']:6}\n")

        file.write("\n")
        daily = defaultdict(lambda: {'rev': 0, 'count': 0, 'customers': set()})

        for t in transactions:
            date = t['Date']
            daily[date]['rev'] += t['Quantity'] * t['UnitPrice']
            daily[date]['count'] += 1
            daily[date]['customers'].add(t['CustomerID'])

        file.write("DAILY SALES TREND\n")
        file.write("-" * 45 + "\n")
        file.write("Date         Revenue   Transactions  Unique Customers\n")

        for date in sorted(daily):
            d = daily[date]
            file.write(f"{date} ₹{d['rev']:8,.0f} {d['count']:14} {len(d['customers']):17}\n")

        file.write("\n")
        success = [t for t in enriched_transactions if t.get('API_Match')]
        failed = [t['ProductName'] for t in enriched_transactions if not t.get('API_Match')]

        file.write("API ENRICHMENT SUMMARY\n")
        file.write("-" * 45 + "\n")
        file.write(f"Total Enriched: {len(success)}\n")
        file.write(f"Success Rate: {(len(success)/len(enriched_transactions))*100:.2f}%\n")
        file.write("Failed Products:\n")

        for p in set(failed):
            file.write(f"- {p}\n")










import requests

def fetch_product_info(product_id):
    """
    Mock API handler (no external dependency).
    """
    return {
        "product_id": product_id,
        "category": "Electronics"
    }

#Task 3.1 (a)

def fetch_all_products():
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        # Checks if the request was successful (status code 200)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        cleaned_products = []

        for p in products:
            cleaned_products.append({
                "id": p.get("id"),
                "title": p.get("title"),
                "category": p.get("category"),
                "brand": p.get("brand"), # Note: some products might not have a brand
                "price": p.get("price"),
                "rating": p.get("rating")
            })

        print(f"Successfully fetched {len(cleaned_products)} products")
        return cleaned_products

    except requests.exceptions.RequestException as e:
        print(f"API fetch failed: {e}")
        return []

# Example of how to call the function:
# all_products = fetch_all_products()
# print(all_products[0])

#Task 3.1 (b)
def create_product_mapping(api_products):
    mapping = {}

    for product in api_products:
        # Map by title (lowercased for case-insensitive matching)
        title_key = product["title"].lower()
        mapping[title_key] = {
            "id": product["id"],
            "category": product["category"],
            "brand": product["brand"],
            "rating": product["rating"]
        }

    return mapping

#Task 3.2 Enrich Sales Data
def enrich_sales_data(transactions, product_mapping):
    enriched = []

    for tx in transactions:
        new_tx = tx.copy()

        try:
            product_num_id = int(tx["ProductID"].replace("P", ""))
        except ValueError:
            product_num_id = None

        if product_num_id in product_mapping:
            api_info = product_mapping[product_num_id]
            new_tx["API_Category"] = api_info["category"]
            new_tx["API_Brand"] = api_info["brand"]
            new_tx["API_Rating"] = api_info["rating"]
            new_tx["API_Match"] = True
        else:
            new_tx["API_Category"] = None
            new_tx["API_Brand"] = None
            new_tx["API_Rating"] = None
            new_tx["API_Match"] = False

        enriched.append(new_tx)

    save_enriched_data(enriched)
    return enriched


#Save Enrich Data to File
def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as file:
        file.write("|".join(headers) + "\n")

        for tx in enriched_transactions:
            row = []
            for h in headers:
                value = tx.get(h)
                row.append("" if value is None else str(value))
            file.write("|".join(row) + "\n")

    print(f"Enriched data saved to {filename}")


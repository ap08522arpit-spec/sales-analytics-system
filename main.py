from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import generate_sales_report
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data


def main():
    try:
        print("=" * 40)
        print("        SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # STEP 1: Read data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # STEP 2: Parse & clean
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")

        # STEP 3: Show filter options
        regions = sorted(set(t['Region'] for t in transactions))
        amounts = [t['Quantity'] * t['UnitPrice'] for t in transactions]

        print("\n[3/10] Filter Options Available:")
        print("Regions:", ", ".join(regions))
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")

        choice = input("Do you want to filter data? (y/n): ").strip().lower()

        if choice == 'y':
            region = input("Enter region (or press Enter to skip): ").strip()
            min_amt = input("Enter minimum amount (or press Enter): ").strip()
            max_amt = input("Enter maximum amount (or press Enter): ").strip()

            region = region if region else None
            min_amt = float(min_amt) if min_amt else None
            max_amt = float(max_amt) if max_amt else None
        else:
            region = min_amt = max_amt = None

        # STEP 4: Validate & filter
        print("\n[4/10] Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(
            transactions,
            region=region,
            min_amount=min_amt,
            max_amount=max_amt
        )
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")

        # STEP 5: Analysis (already done via report)
        print("\n[5/10] Analyzing sales data...")
        print("✓ Analysis complete")

        # STEP 6: API fetch
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # STEP 7: Enrichment
        print("\n[7/10] Enriching sales data...")
        product_map = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(valid_transactions, product_map)
        success_count = sum(1 for t in enriched_transactions if t.get('API_Match'))
        print(f"✓ Enriched {success_count}/{len(enriched_transactions)} transactions")

        # STEP 8: Save enriched data (already saved in function)
        print("\n[8/10] Saving enriched data...")
        print("✓ Saved to: data/enriched_sales_data.txt")

        # STEP 9: Generate report
        print("\n[9/10] Generating report...")
        generate_sales_report(valid_transactions, enriched_transactions)
        print("✓ Report saved to: output/sales_report.txt")

        # STEP 10: Finish
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n ERROR OCCURRED")
        print("Something went wrong:", str(e))


if __name__ == "__main__":
    main()

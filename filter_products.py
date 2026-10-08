import json
import os

def main():
    with open("products_to_upload.json", "r", encoding="utf-8") as f:
        products = json.load(f)
        
    valid_products = []
    missing_data_products = []
    
    for p in products:
        # Check required fields: name, cost_price, sale_price, image_path
        has_name = bool(p.get("name") and p["name"].strip())
        has_cost = bool(p.get("cost_price") and p["cost_price"].strip())
        has_sale = bool(p.get("sale_price") and p["sale_price"].strip())
        has_image = bool(p.get("image_path") and os.path.exists(p["image_path"]))
        
        if has_name and has_cost and has_sale and has_image:
            valid_products.append(p)
        else:
            missing_data_products.append(p)
            
    # Save the filtered list
    with open("filtered_products_to_upload.json", "w", encoding="utf-8") as f:
        json.dump(valid_products, f, indent=4)
        
    print(f"Original product count: {len(products)}")
    print(f"Valid products (with image and all data): {len(valid_products)}")
    print(f"Skipped products: {len(missing_data_products)}")
    
    # Save a report of skipped items so the user knows what was missed
    with open("skipped_products_report.txt", "w", encoding="utf-8") as f:
        f.write("PRODUCTS SKIPPED DUE TO MISSING DATA OR IMAGE:\n")
        f.write("="*50 + "\n")
        for p in missing_data_products:
            reason = []
            if not bool(p.get("name")): reason.append("Missing Name")
            if not bool(p.get("cost_price")): reason.append("Missing Cost Price")
            if not bool(p.get("sale_price")): reason.append("Missing Sale Price")
            if not bool(p.get("image_path") and os.path.exists(p.get("image_path", ""))): reason.append("Missing/Unmatched Image")
            
            f.write(f"- {p.get('name', 'UNKNOWN')} | Reason: {', '.join(reason)}\n")

if __name__ == "__main__":
    main()


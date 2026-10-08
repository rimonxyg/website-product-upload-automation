import json
import os
import re
from datetime import datetime
import difflib

def clean_price(price_str):
    return re.sub(r'[^\d.]', '', price_str)

def get_shelf_life(date_str):
    if not date_str or date_str == '-' or date_str.strip() == '':
        return ""
    try:
        # Some dates might be DD-MM-YYYY
        exp_date = datetime.strptime(date_str.strip(), "%d-%m-%Y")
        today = datetime.now()
        days = (exp_date - today).days
        return str(max(0, days)) # Don't return negative shelf life
    except Exception as e:
        return ""

def main():
    # Load all available images
    image_dir = "o_mama_pictures"
    available_images = os.listdir(image_dir)
    image_names_without_ext = {os.path.splitext(img)[0]: img for img in available_images}
    
    products = []
    
    with open("product_list.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    # Skip header
    started = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "Product" in line and "Unit Purchase Price" in line:
            started = True
            continue
        if "Add to location" in line:
            break
            
        if started:
            # Layout might have multiple spaces between columns
            parts = re.split(r'\s{2,}|\t', line)
            if len(parts) >= 3:
                name = parts[0].strip()
                cost_price = clean_price(parts[1])
                sale_price = clean_price(parts[2])
                expiry_date = parts[3].strip() if len(parts) > 3 else ""
                
                if expiry_date == '-':
                    expiry_date = ""
                if len(expiry_date) > 10:
                    expiry_date = expiry_date[:10] # Grab just the date part if merged with editor name
                
                shelf_life = get_shelf_life(expiry_date)
                
                # Match image
                image_path = ""
                # 1. Exact match without extension
                if name in image_names_without_ext:
                    image_path = os.path.abspath(os.path.join(image_dir, image_names_without_ext[name]))
                else:
                    # 2. Cleaned name match
                    clean_name = name.replace("_", " ").lower()
                    for img_no_ext, img_full in image_names_without_ext.items():
                        if clean_name == img_no_ext.replace("_", " ").lower():
                            image_path = os.path.abspath(os.path.join(image_dir, img_full))
                            break
                    
                    # 3. Fuzzy match
                    if not image_path:
                        matches = difflib.get_close_matches(name, image_names_without_ext.keys(), n=1, cutoff=0.6)
                        if matches:
                            image_path = os.path.abspath(os.path.join(image_dir, image_names_without_ext[matches[0]]))
                
                products.append({
                    "name": name,
                    "cost_price": cost_price,
                    "sale_price": sale_price,
                    "shelf_life": shelf_life,
                    "image_path": image_path
                })
                
    # Save to JSON
    with open("products_to_upload.json", "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4)
        
    print(f"Parsed {len(products)} products. Saved to products_to_upload.json")

if __name__ == "__main__":
    main()


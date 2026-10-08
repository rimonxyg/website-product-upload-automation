# SOHUB Product Automation Scripts

This folder contains all the scripts and data generated to automate uploading products to the SOHUB Machines Portal.

## 📁 Files & Purpose

### Data & Configuration
1. **`auth_state.json`** - Contains your saved browser login session. The scripts use this so you don't have to log in manually every time. (Keep this file secure).
2. **`rm product list 0001.pdf`** - The original PDF containing the product list.
3. **`product_list.txt`** - The raw text extracted from the PDF.
4. **`products_to_upload.json`** - The fully parsed data linking the PDF info to the `o_mama_pictures` images.
5. **`filtered_products_to_upload.json`** - The strict, cleaned list containing ONLY products that have ALL required prices and a matching image. (This is what actually gets uploaded).
6. **`skipped_products_report.txt`** - A text file telling you exactly which products were skipped and *why* (e.g. missing image, missing price).
7. **`upload_results.csv`** - The final log showing "Success", "Failed", or "Skipped (Duplicate)" for every upload attempt.

### Python Scripts
1. **`prepare_data.py`** 
   - **What it does:** Reads the PDF text, extracts the names, prices, and expiry dates, calculates the shelf life in days, and fuzzy-matches the names to the images in the `o_mama_pictures` folder. 
   - **Run when:** You have a new PDF or new images and need to generate a fresh `products_to_upload.json`.
2. **`filter_products.py`** 
   - **What it does:** Scans `products_to_upload.json` and throws out any product that is missing an image or a price. Creates `filtered_products_to_upload.json`.
   - **Run when:** You want to ensure only 100% complete products are uploaded.
3. **`bulk_upload.py`** 
   - **What it does:** The main automation bot. It opens the browser, checks the portal's search bar to make sure the product doesn't already exist, fills the form, uploads the image, and saves.
   - **Run when:** You are ready to actually push the data to the portal.
4. **`inspect_portal.py` & `extract_form.py`** - Setup scripts we used initially to grab the HTML and your login session. 

## 🚀 How to use this in the future

If you get a new batch of products next week, follow these exact steps:

1. Put your new images in the `o_mama_pictures` folder.
2. Put your new PDF text into `product_list.txt`.
3. Activate the environment:
   ```bash
   source venv/bin/activate
   ```
4. Prepare the data:
   ```bash
   python3 prepare_data.py
   ```
5. Filter out the bad/missing data:
   ```bash
   python3 filter_products.py
   ```
6. Check `skipped_products_report.txt` to see if you forgot to download any images.
7. Run the upload bot:
   ```bash
   python3 bulk_upload.py
   ```

## ⚠️ Important Rules Established
- **No Hallucination/Guessing:** Category and Unit dropdowns are left blank to avoid assuming the wrong classification. 
- **Image Mandatory:** If a product does not have a matching image, it will be skipped entirely.
- **Duplicate Protection:** The bot will always type the product name into the portal's search bar first. If a result shows up, it skips the product.


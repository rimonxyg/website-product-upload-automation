# SOHUB Products Bulk Uploader - Developer Quick Start

This guide is designed for developers stepping in to run or maintain the SOHUB Bulk Uploader. 

The tool uses **Python & Playwright** to read a PDF, match product names to local images using fuzzy string matching, and automate the frontend UI of the SOHUB portal (since no backend API access or native CSV bulk upload is available).

---

## 🛠 Architecture & Workflow
1. **Data Prep (`prepare_data.py`)**: Parses the `product_list.txt` (extracted from the PDF), formats prices, calculates the shelf life (in days) from the expiry date, and maps the product to an image in the `o_mama_pictures/` folder. Outputs `products_to_upload.json`.
2. **Sanitization (`filter_products.py`)**: Filters the JSON to ensure no product is uploaded without a valid image or price. Outputs `filtered_products_to_upload.json`.
3. **Bot Execution (`bulk_upload.py`)**: Uses Playwright to iterate through the filtered JSON, search the portal to prevent duplicates, fill out the modal form, upload the image, and save. Logs results to `upload_results.csv`.

---

## 🚀 Quick Start (Linux/Mac)

If you have a fresh batch of products to upload, follow these steps:

### 1. Setup Environment
Ensure Python 3.10+ is installed.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

### 2. Authenticate Session (One-Time)
Run the inspector script to save the auth tokens/cookies locally:
```bash
python3 inspect_portal.py
```
*A browser will open. Log into the SOHUB portal manually. Once you see the products dashboard, go back to the terminal and press `ENTER`. This saves `auth_state.json`.*

### 3. Load New Data
1. Place the new images inside the `o_mama_pictures/` folder.
2. If you received a new PDF, extract the text and save it as `product_list.txt`:
   ```bash
   pdftotext -layout new_products.pdf product_list.txt
   ```

### 4. Run the Pipeline
Execute the data processing and upload scripts in order:

```bash
# 1. Parse text and match images
python3 prepare_data.py

# 2. Filter out products missing mandatory data/images
python3 filter_products.py

# 3. Watch the bot upload the valid products (Checks for duplicates automatically)
python3 bulk_upload.py
```

---

## 🐛 Troubleshooting

* **Missing Images:** If `filter_products.py` skips a lot of items, check `skipped_products_report.txt`. The fuzzy matching relies on the image filename being somewhat similar to the product name in the PDF.
* **Playwright Timeouts:** If the portal is running slow, Playwright might time out waiting for the "New product" modal. You can increase the `timeout=5000` values inside `bulk_upload.py`.
* **Session Expired:** If the bot immediately fails to find the search bar or products page, your session token expired. Re-run `python3 inspect_portal.py` to get a fresh `auth_state.json`.


# BULK UPLOAD RUNBOOK (COPY/PASTE)

## 1. FIRST TIME SETUP (Run once)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## 2. LOGIN (Run when session expires)
```bash
source venv/bin/activate
python3 inspect_portal.py
```
*(A browser opens. Log in. Go back to terminal and press ENTER to save session).*

## 3. LOAD NEW DATA
1. Put new images in `o_mama_pictures/`
2. Extract new PDF text:
```bash
pdftotext -layout <YOUR_PDF_FILE>.pdf product_list.txt
```

## 4. RUN PIPELINE (Run every time you have new data)
```bash
source venv/bin/activate
python3 prepare_data.py
python3 filter_products.py
python3 bulk_upload.py
```

*(Check `skipped_products_report.txt` for any items that failed validation, and `upload_results.csv` for final upload status).*


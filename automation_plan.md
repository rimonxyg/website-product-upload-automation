# Product Upload Automation Plan

## Goal
Automate the addition of ~60 products and their local images to the SOHUB Machines portal (https://portal.machines.sohub.com.bd/workspace/products) using an authorized account, without manual entry.

## Current Status
- [x] Received PDF with ~89 product entries.
- [x] Received `o_mama_pictures` folder with images.
- [x] Portal inspected securely via Python + Playwright using user's authenticated session.

## Discoveries & Recommendations

### 1. Portal Discoveries
The SOHUB portal is a modern Single Page Application (SPA). To add a product, you must click a "New product" button which opens a modal containing the product form. 

### 2. Native Bulk Upload Existence
There is **no** native Excel/CSV bulk upload button available in the portal UI for Products.

### 3. Browser Automation Feasibility
**Highly Feasible.** Using Python + Playwright works perfectly. We successfully launched a browser, logged in, and preserved the authentication state. 

### 4. Authorized API Availability
While the SPA uses an internal API, the safest approach that completely avoids bypassing CSRF/auth tokens is to use Playwright to drive the UI exactly as a human would.

### 5. Required Form Fields
The product form requires the following fields:
- **Name** (Required)
- **Cost price ৳** (Required)
- **Sale price ৳** (Required)
- **Category** (Optional Dropdown)
- **Unit** (Optional Dropdown)
- **Shelf life (days)** (Optional)
- **Net weight / volume & Measure** (Optional)
- **SKU** (Optional, auto-generates if blank)
- **Barcode** (Optional)

### 6. Image Upload Mechanics
The image upload is an invisible `<input type="file" accept="image/*">` element. Playwright can interact directly with this element using `page.set_input_files()`.

### 7. PDF -> Portal Field Mapping
| PDF Column | Portal Field | Notes |
| :--- | :--- | :--- |
| Product | Name | |
| Unit Purchase Price | Cost price ৳ | Extract numeric value (remove '৳') |
| Selling Price | Sale price ৳ | Extract numeric value (remove '৳') |
| Expiry Date | Shelf life (days) | Must calculate the number of days from *today* to the Expiry Date. |

### 8. Image -> Product Matching Method
We will use **Fuzzy String Matching** (`difflib` in Python).
Example: PDF Name `Aarong_Chocolate_Milk` will automatically match the file `o_mama_pictures/Aarong_Chocolate_Milk.png`.

### 9. Recommended Automation Architecture
**Option C: Python + Playwright browser automation** using the `auth_state.json` we just created.
- **Data Source:** Extract table from `rm product list 0001.pdf` using `pdfplumber` or `PyPDF2`.
- **Bot Engine:** Playwright scripts in headless mode.
- **Reporting:** Save results (Success/Failure/Errors) to a CSV log.

### 10. Required Files
We have everything we need:
- `rm product list 0001.pdf`
- `o_mama_pictures/` folder
- `auth_state.json` (Playwright session)

### 11. Test Plan for ONE Product
Before running all 60+ products, we will run a test script (`test_one_product.py`) that will:
1. Parse the first valid product from the PDF (e.g., `Kurkure_Cream_Onion_Chips`).
2. Calculate the Expiry Days from today.
3. Match it to `o_mama_pictures/Kurkure_Cream_Onion_Chips.png` (or `.jpg`).
4. Open the Playwright browser (Visible mode, so you can watch).
5. Click "New product".
6. Fill in the extracted fields.
7. Upload the matching image.
8. Click "Create product".
9. Verify the product appears in the list.

### 12. Awaiting Approval
**I will not execute the test script until you explicitly approve.**

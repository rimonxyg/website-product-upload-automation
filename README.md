# 🚀 Website Product Upload Automation

Welcome to the **Website Product Upload Automation** project! 

This repository contains a fully automated bot designed to read product details from a PDF/JSON, match them with local images, and automatically upload them to your website portal using a simulated browser (Playwright). 

It is designed to be **100% idiot-proof** with "one-click" batch scripts so that normal users, managers, and non-technical staff can run it effortlessly!

---

## 🌟 Key Features
- **🤖 Automated Browser:** Physically opens a browser and types data in to completely bypass complicated backend API setups.
- **🛡️ Duplicate Protection:** Intelligently searches your website *before* uploading to guarantee no duplicates are ever created.
- **🧩 Smart Fuzzy Matching:** Automatically pairs the name on the PDF (e.g. "Coca Cola") to the image file in your folder (e.g. `coca_cola.jpg`).
- **📝 Automatic Validation:** Rejects any products missing mandatory prices or images to keep your database perfectly clean.
- **🖱️ 1-Click "Auto-Run" Setup:** Designed for normal users with simple `.bat` files!

---

## 💻 How to Use (For Normal Users on Windows)

We've set up three simple "Auto-Run" files so you don't have to touch a single line of code.

### Step 1: Install & Setup (Run Once)
Double-click the **`setup.bat`** file. 
Wait a few minutes while it automatically downloads the required Python environment and the virtual browser. 

### Step 2: Log into the Website (Run Once)
Double-click the **`1_login.bat`** file. 
A browser window will pop open. Simply log into your website portal using your credentials. Once you see your dashboard, go back to the black terminal screen and press **ENTER**. The bot will securely memorize your session so you don't have to log in again!

### Step 3: Run the Bot! (Run every time you have new data)
1. Drop your new product images into the `o_mama_pictures/` folder.
2. Replace `product_list.txt` with your new data.
3. Double-click the **`2_run_bot.bat`** file!

Sit back and watch! The bot will sort through your data, throw out the bad items, open the browser, and upload everything safely. When it finishes, you can check `upload_results.csv` for a full report!

---

## 🛠 For Developers
If you want to view the source code, check out the Python files (`bulk_upload.py`, `prepare_data.py`, `filter_products.py`).

For a quick breakdown of the architecture, check out **`2_Developer_Manual.md`** and the quick-commands in **`3_Developer_Runbook.md`**.

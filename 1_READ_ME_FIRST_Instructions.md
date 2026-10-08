# SOHUB Bulk Upload Bot - Manager Guide

This package automates the bulk uploading of products to the SOHUB portal. 

## Requirements
- Python 3.10+ installed on your computer.

## One-Time Setup
1. Double click **`setup.bat`** (Windows). This will download the virtual browser and dependencies. It might take a few minutes.
2. Double click **`1_login.bat`**. A browser will open. Log into the SOHUB portal. Once logged in, go back to the black terminal screen and press **ENTER**. This securely saves your session so you don't have to log in again.

## How to use (Daily/Weekly)
Whenever you have a new batch of products:
1. Place your new PDF containing the product list into the folder, renaming it if necessary, but you must extract the text to `product_list.txt`. (Or overwrite `product_list.txt` with your data).
2. Place all the new images into the `o_mama_pictures` folder.
3. Double click **`2_run_bot.bat`**. 

The bot will:
- Match the products to the images.
- Skip anything missing a price or an image.
- Open the browser.
- Check if the product already exists (to avoid duplicates).
- Fill the form and upload the image.
- Save a report to `upload_results.csv`.


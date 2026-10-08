import asyncio
import json
import csv
import os
from playwright.async_api import async_playwright

async def main():
    with open("filtered_products_to_upload.json", "r", encoding="utf-8") as f:
        products = json.load(f)
        
    print(f"Loaded {len(products)} products from JSON.")
    
    # Setup CSV logging
    csv_file = open("upload_results.csv", "w", newline="", encoding="utf-8")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Name", "Status", "Message"])
    
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=False, slow_mo=200) # Slower for reliability
        context = await browser.new_context(storage_state="auth_state.json")
        page = await context.new_page()
        
        await page.goto("https://your-company-portal.com/workspace/products")
        
        for i, product in enumerate(products):
            print(f"\n[{i+1}/{len(products)}] Processing: {product['name']}")
            
            try:
                # 1. Search to check if it exists
                search_input = page.get_by_placeholder("Search SKU, name, category…")
                await search_input.fill(product['name'])
                await page.wait_for_timeout(2000) # wait for results
                
                # Check if it exists in the table
                # The name is usually in a <td>
                existing_item = page.locator(f"td:has-text(\"{product['name']}\")")
                count = await existing_item.count()
                
                if count > 0:
                    print(f"-> Already exists! Skipping.")
                    csv_writer.writerow([product['name'], "Skipped", "Already exists"])
                    await search_input.fill("") # clear search
                    await page.wait_for_timeout(1000)
                    continue
                    
                # Clear search
                await search_input.fill("")
                await page.wait_for_timeout(1000)
                
                # 2. Click New Product
                print("-> Clicking 'New product'...")
                new_prod_btn = page.get_by_text("New product", exact=True)
                await new_prod_btn.wait_for(state="visible", timeout=5000)
                await new_prod_btn.click()
                
                print("-> Filling form...")
                await page.get_by_role("button", name="Create product").wait_for(state="visible", timeout=5000)
                
                await page.locator('input[name="name"]').fill(product['name'])
                await page.locator('input[name="costPrice"]').fill(product['cost_price'])
                await page.locator('input[name="salePrice"]').fill(product['sale_price'])
                
                if product['shelf_life']:
                    await page.locator('input[name="shelfLifeDays"]').fill(product['shelf_life'])
                    
                if product['image_path'] and os.path.exists(product['image_path']):
                    print("-> Uploading image...")
                    await page.locator('input[type="file"]').set_input_files(product['image_path'])
                else:
                    print("-> No image found or invalid path.")
                    
                # 3. Submit
                print("-> Submitting...")
                await page.get_by_role("button", name="Create product").click()
                
                # 4. Wait for success
                await page.get_by_text("Create product", exact=True).wait_for(state="hidden", timeout=15000)
                print("-> Success!")
                csv_writer.writerow([product['name'], "Success", "Created"])
                
                await page.wait_for_timeout(1000) # brief pause before next
                
            except Exception as e:
                print(f"-> ERROR: {str(e)}")
                csv_writer.writerow([product['name'], "Failed", str(e)])
                
                # Try to recover by closing modal if it's open, or refreshing
                try:
                    cancel_btn = page.get_by_role("button", name="Cancel")
                    if await cancel_btn.count() > 0:
                        await cancel_btn.click()
                    else:
                        await page.reload()
                        await page.wait_for_timeout(3000)
                except:
                    await page.reload()
                    await page.wait_for_timeout(3000)

        await browser.close()
    
    csv_file.close()
    print("\nBulk upload complete! Check upload_results.csv for details.")

if __name__ == "__main__":
    asyncio.run(main())


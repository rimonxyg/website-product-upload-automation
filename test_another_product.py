import asyncio
import os
from datetime import datetime
from playwright.async_api import async_playwright

async def main():
    # TEST DATA 2: Fanta Can
    product_name = "Fanta Can"
    cost_price = "65.00"
    sale_price = "70.00"
    expiry_date_str = "13-01-2027"
    image_path = os.path.abspath("o_mama_pictures/Fanta can.jpg")
    
    # Calculate shelf life
    exp_date = datetime.strptime(expiry_date_str, "%d-%m-%Y")
    today = datetime.now()
    shelf_life_days = str((exp_date - today).days)
    
    print(f"--- TEST DATA ---")
    print(f"Name: {product_name}")
    print(f"Cost Price: ৳{cost_price}")
    print(f"Sale Price: ৳{sale_price}")
    print(f"Shelf Life: {shelf_life_days} days (from {expiry_date_str})")
    print(f"Image: {image_path}")
    print(f"-----------------\n")

    async with async_playwright() as p:
        print("Launching browser with saved session...")
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context(storage_state="auth_state.json")
        page = await context.new_page()
        
        print("Navigating to products page...")
        await page.goto("https://portal.machines.sohub.com.bd/workspace/products")
        
        print("Clicking 'New product' button...")
        new_prod_btn = page.get_by_text("New product", exact=True)
        await new_prod_btn.wait_for(state="visible", timeout=15000)
        await new_prod_btn.click()
        
        print("Waiting for form to render...")
        await page.get_by_role("button", name="Create product").wait_for(state="visible", timeout=10000)
        
        print("Filling form fields...")
        await page.locator('input[name="name"]').fill(product_name)
        await page.locator('input[name="costPrice"]').fill(cost_price)
        await page.locator('input[name="salePrice"]').fill(sale_price)
        await page.locator('input[name="shelfLifeDays"]').fill(shelf_life_days)
        
        print("Uploading image...")
        await page.locator('input[type="file"]').set_input_files(image_path)
        
        print("Waiting 3 seconds for visual confirmation...")
        await page.wait_for_timeout(3000)
        
        print("Submitting form...")
        await page.get_by_role("button", name="Create product").click()
        
        print("Waiting for creation to complete...")
        await page.get_by_text("Create product", exact=True).wait_for(state="hidden", timeout=15000)
        print("✅ Fanta Can created successfully!")
        
        await page.wait_for_timeout(3000)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())


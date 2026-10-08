import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        print("Launching browser with saved session...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state="auth_state.json")
        page = await context.new_page()
        
        url = "https://portal.machines.sohub.com.bd/workspace/products"
        print(f"Navigating to {url} ...")
        await page.goto(url)
        
        print("Waiting for 'New product' button...")
        # Get button exactly matching 'New product'
        new_prod_btn = page.get_by_text("New product", exact=True)
        await new_prod_btn.wait_for(state="visible", timeout=15000)
        
        print("Clicking 'New product' button...")
        await new_prod_btn.click()
        
        # Wait for the form modal or page to load. Let's wait for a 'Save' or 'Cancel' button.
        print("Waiting for form to render...")
        try:
            await page.get_by_role("button", name="Save").wait_for(state="visible", timeout=5000)
        except:
            await page.wait_for_timeout(3000) # Fallback wait
        
        print("Extracting form HTML...")
        form_html = await page.content()
        with open("new_product_form.html", "w", encoding="utf-8") as f:
            f.write(form_html)
            
        print("Saved to new_product_form.html!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())


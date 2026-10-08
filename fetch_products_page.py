import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        print("Launching browser with saved session...")
        browser = await p.chromium.launch(headless=True)
        # Use the saved authentication state!
        context = await browser.new_context(storage_state="auth_state.json")
        page = await context.new_page()
        
        url = "https://portal.machines.sohub.com.bd/workspace/products"
        print(f"Navigating directly to {url} ...")
        await page.goto(url)
        
        # Wait a moment for dynamic content to load (like React/Vue fetching data)
        await page.wait_for_timeout(3000)
        
        print("Extracting products page HTML...")
        html = await page.content()
        with open("products_html.txt", "w", encoding="utf-8") as f:
            f.write(html)
            
        # Try to find an "Add Product" button and click it to dump the form as well
        try:
            print("Looking for an 'Add Product' or 'New Product' button...")
            # Common text for add buttons
            button = page.get_by_role("button", name="Add Product")
            if await button.count() == 0:
                button = page.get_by_text("Add Product", exact=True)
            if await button.count() == 0:
                button = page.get_by_text("New Product", exact=True)
                
            if await button.count() > 0:
                print("Found Add/New product button! Clicking it...")
                await button.first.click()
                await page.wait_for_timeout(2000)
                
                print("Extracting form HTML...")
                form_html = await page.content()
                with open("form_html.txt", "w", encoding="utf-8") as f:
                    f.write(form_html)
            else:
                print("Could not find an obvious 'Add Product' button.")
        except Exception as e:
            print("Error finding/clicking add button:", e)
            
        await browser.close()
        print("Done!")

if __name__ == "__main__":
    asyncio.run(main())


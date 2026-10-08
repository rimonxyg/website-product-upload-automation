import asyncio
from playwright.async_api import async_playwright
import re

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state="auth_state.json")
        page = await context.new_page()
        
        url = "https://portal.machines.sohub.com.bd/workspace/products"
        print(f"Navigating to {url} ...")
        await page.goto(url)
        
        # Wait for the "Loading..." text to disappear
        try:
            await page.get_by_text("Loading…").wait_for(state="hidden", timeout=10000)
        except Exception:
            print("Loading text didn't hide, or already hidden.")
            
        await page.wait_for_timeout(3000)
        
        html = await page.content()
        with open("current_products.html", "w", encoding="utf-8") as f:
            f.write(html)
            
        # Let's try to grab all text from table cells or divs that look like product names
        # We can just extract all text in the body and print a sample
        print("Scraped page.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())


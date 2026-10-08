import asyncio
from playwright.async_api import async_playwright
import sys

async def main():
    async with async_playwright() as p:
        print("Launching browser...")
        # Launch headed browser so you can log in
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        url = "https://your-company-portal.com/workspace/products"
        print(f"Navigating to {url} ...")
        await page.goto(url)
        
        print("\n" + "="*50)
        print("PLEASE LOG IN TO THE PORTAL IN THE OPENED BROWSER.")
        print("Once you are logged in and can see the 'Products' page,")
        print("PRESS ENTER IN THIS TERMINAL TO CONTINUE.")
        print("="*50 + "\n")
        
        # Wait for user input in the terminal (async safe)
        await asyncio.to_thread(input)
        
        print("Saving authentication state for later use...")
        await context.storage_state(path="auth_state.json")
        
        print("Extracting page HTML for inspection...")
        html = await page.content()
        with open("portal_html.txt", "w", encoding="utf-8") as f:
            f.write(html)
            
        print("Done! You can close the browser now.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())


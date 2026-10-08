import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state="auth_state.json")
        page = await context.new_page()
        await page.goto("https://portal.machines.sohub.com.bd/workspace/products")
        await page.wait_for_timeout(3000)
        print("Final URL:", page.url)
        await browser.close()
asyncio.run(main())

import asyncio
import os
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def run():
    async with async_playwright() as p:
        user_data_dir = os.path.join(os.getcwd(), "browser_profile")
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=True,
            channel="chrome",
            viewport={'width': 1920, 'height': 1080},
        )

        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        
        await page.goto("https://seller-us.tiktok.com/compass/data-overview?shop_region=US", wait_until="networkidle")
        await asyncio.sleep(5)

        # Click "Product analytics"
        print("Clicking 'Product analytics'...")
        await page.get_by_text("Product analytics", exact=True).click()
        
        # WAITING LONGER FOR DATA LOAD
        print("Waiting 15 seconds for product data to populate...")
        await asyncio.sleep(15)

        # Scroll to middle and bottom to trigger all lazy loads
        await page.evaluate("window.scrollTo(0, 1000)")
        await asyncio.sleep(5)
        await page.evaluate("window.scrollTo(0, 2000)")
        await asyncio.sleep(5)

        # Final Captures
        os.makedirs("exploration", exist_ok=True)
        await page.screenshot(path="exploration/product_analytics_final.png", full_page=True)
        
        content = await page.content()
        with open("exploration/product_analytics_final.html", "w") as f:
            f.write(content)
            
        text = await page.evaluate("document.body.innerText")
        with open("exploration/product_analytics_final_text.txt", "w") as f:
            f.write(text)
            
        print("✅ Final Product Analytics captures saved.")
        await context.close()

if __name__ == "__main__":
    asyncio.run(run())

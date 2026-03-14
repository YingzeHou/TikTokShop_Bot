import asyncio
import os
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def run():
    state_path = os.path.join(os.getcwd(), "session_state.json")
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
        
        target_url = "https://seller-us.tiktok.com/compass/data-overview?shop_region=US"
        print(f"Opening {target_url} to dump all text...")
        await page.goto(target_url, wait_until="networkidle")
        
        # Dismiss any overlays
        try:
            await page.get_by_text("Got it").click()
            await asyncio.sleep(2)
        except: pass

        # Scroll a bit
        await page.evaluate("window.scrollTo(0, 500)")
        await asyncio.sleep(5)

        # Get all text content
        text_content = await page.evaluate("document.body.innerText")
        
        with open("exploration/page_text_dump.txt", "w", encoding="utf-8") as f:
            f.write(text_content)
        
        print("✅ Page text dumped to exploration/page_text_dump.txt")
        
        # Print first 1000 chars for a quick look
        print("\n--- Preview of Page Text ---")
        print(text_content[:1000])

        await context.close()

if __name__ == "__main__":
    asyncio.run(run())

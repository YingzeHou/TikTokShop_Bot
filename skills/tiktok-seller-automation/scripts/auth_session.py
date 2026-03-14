import asyncio
import os
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Using a common user agent to look more like a standard browser
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        
        browser = await p.chromium.launch(headless=False)
        # Setting a larger viewport and the user agent
        context = await browser.new_context(
            user_agent=user_agent,
            viewport={'width': 1280, 'height': 800}
        )

        page = await context.new_page()
        print("Opening TikTok Shop Seller Center...")
        
        # Navigate and wait for the page to be fully loaded
        await page.goto("https://seller-us.tiktok.com/account/login", wait_until="networkidle")

        print("\n*** ACTION REQUIRED ***")
        print("1. Log in manually in the browser window.")
        print("2. Complete any 2FA or Captchas.")
        print("3. Once you see the main Dashboard, come back here.")
        
        input("\nPress Enter here AFTER you are fully logged in and see the dashboard...")

        # Save storage state to the project root
        state_path = os.path.join(os.getcwd(), "session_state.json")
        await context.storage_state(path=state_path)
        
        print(f"\n✅ Session state successfully saved to {state_path}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

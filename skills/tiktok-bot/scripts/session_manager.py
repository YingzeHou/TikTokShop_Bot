import asyncio
import os
import json
from playwright.async_api import async_playwright

# File path to store the full session state (cookies + local storage)
SESSION_FILE = "session_state.json"
LOGIN_URL = "https://seller-us.tiktok.com/"
ADS_DASHBOARD_URL = "https://ads.tiktok.com/i18n/gmv-max/dashboard?aadvid=7383481422339735568&oec_seller_id=7495613311299782811&bc_id=7312519670601400321"

async def manage_session():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        session_map = {}

        # 1. Login to Seller Center
        print(f"\n--- STEP 1: Seller Center ---")
        print(f"Navigating to {LOGIN_URL}...")
        await page.goto(LOGIN_URL)
        print("\nACTION REQUIRED: Please log in to the Seller Center in the browser window.")
        input("Press Enter in this terminal ONLY AFTER you have reached the homepage/dashboard...")
        session_map["seller_center"] = await context.storage_state()
        print("Seller Center session captured.")

        # 2. Login to Ads Center
        print(f"\n--- STEP 2: Ads Center ---")
        print(f"Navigating to {ADS_DASHBOARD_URL}...")
        await page.goto(ADS_DASHBOARD_URL)
        print("\nACTION REQUIRED: Please log in to the Ads Center in the browser window.")
        input("Press Enter in this terminal ONLY AFTER you have reached the ads dashboard...")
        session_map["ads_center"] = await context.storage_state()
        print("Ads Center session captured.")

        # Save the mapped session state
        with open(SESSION_FILE, "w") as f:
            json.dump(session_map, f, indent=4)
        
        print(f"\nSuccessfully saved mapped session state to {SESSION_FILE}")
        await browser.close()

if __name__ == "__main__":
    # Standard asyncio run
    asyncio.run(manage_session())

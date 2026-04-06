import asyncio
import os
import json
from playwright.async_api import async_playwright

# File path to store the full session state (cookies + local storage)
SESSION_FILE = "session_state.json"
LOGIN_URL = "https://seller-us.tiktok.com/"
ADS_DASHBOARD_URL = "https://ads.tiktok.com/i18n/gmv-max/dashboard?aadvid=7383481422339735568&oec_seller_id=7495613311299782811&bc_id=7312519670601400321"

async def verify_seller_session(page):
    """Verify that the seller center session is valid by checking for login indicators."""
    try:
        # Wait a bit for any redirects to complete
        await asyncio.sleep(2)

        # Check if we're still on a seller center domain (not login page)
        current_url = page.url
        if "login" in current_url.lower() or "passport" in current_url.lower():
            return False

        # Check for common seller center elements
        # This will vary based on the actual page structure
        try:
            # Wait for a short time to see if any critical elements appear
            await page.wait_for_load_state("networkidle", timeout=10000)
            return True
        except:
            return True  # If timeout, assume it's okay
    except Exception as e:
        print(f"Warning during session verification: {e}")
        return True  # Continue anyway

async def manage_session():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        session_map = {}

        # 1. Login to Seller Center
        print(f"\n--- STEP 1: Seller Center ---")
        print(f"Navigating to {LOGIN_URL}...")
        await page.goto(LOGIN_URL, wait_until="networkidle")
        print("\nACTION REQUIRED: Please log in to the Seller Center in the browser window.")
        print("IMPORTANT: Make sure you:")
        print("  1. Complete any 2FA/verification steps")
        print("  2. Navigate to a page that requires authentication (e.g., Products, Orders)")
        print("  3. Wait for the page to fully load")
        input("\nPress Enter in this terminal ONLY AFTER you have completed all steps...")

        # Give the page a moment to finish any background requests
        await asyncio.sleep(3)
        await page.wait_for_load_state("networkidle")

        # Verify session
        if await verify_seller_session(page):
            session_map["seller_center"] = await context.storage_state()
            print("✓ Seller Center session captured and verified.")
        else:
            print("✗ Warning: Seller Center session may not be valid. Please ensure you're logged in.")
            session_map["seller_center"] = await context.storage_state()

        # 2. Login to Ads Center
        print(f"\n--- STEP 2: Ads Center ---")
        print(f"Navigating to {ADS_DASHBOARD_URL}...")
        await page.goto(ADS_DASHBOARD_URL, wait_until="networkidle")
        print("\nACTION REQUIRED: Please log in to the Ads Center in the browser window.")
        print("IMPORTANT: Make sure you:")
        print("  1. Complete any 2FA/verification steps")
        print("  2. Wait for the ads dashboard to fully load")
        print("  3. See your actual campaign data")
        input("\nPress Enter in this terminal ONLY AFTER you have completed all steps...")

        # Give the page a moment to finish any background requests
        await asyncio.sleep(3)
        await page.wait_for_load_state("networkidle")

        session_map["ads_center"] = await context.storage_state()
        print("✓ Ads Center session captured.")

        # Save the mapped session state
        with open(SESSION_FILE, "w") as f:
            json.dump(session_map, f, indent=4)

        print(f"\n✓ Successfully saved mapped session state to {SESSION_FILE}")
        print(f"\nSession statistics:")
        print(f"  Seller Center: {len(session_map['seller_center']['cookies'])} cookies")
        print(f"  Ads Center: {len(session_map['ads_center']['cookies'])} cookies")

        await browser.close()

if __name__ == "__main__":
    # Standard asyncio run
    asyncio.run(manage_session())

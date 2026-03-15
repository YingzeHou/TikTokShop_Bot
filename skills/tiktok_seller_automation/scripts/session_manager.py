import asyncio
import os
from playwright.async_api import async_playwright

# File path to store the full session state (cookies + local storage)
SESSION_FILE = "session_state.json"
LOGIN_URL = "https://seller-us.tiktok.com/login"
DASHBOARD_URL = "https://seller-us.tiktok.com/homepage"

async def manage_session():
    async with async_playwright() as p:
        # Launch browser - headless=False so you can see it if manual login is needed
        browser = await p.chromium.launch(headless=False)
        
        # Check if we have an existing session
        if os.path.exists(SESSION_FILE):
            print(f"Found existing session at {SESSION_FILE}. Attempting to use it...")
            context = await browser.new_context(storage_state=SESSION_FILE)
        else:
            print("No existing session found. Starting fresh...")
            context = await browser.new_context()

        page = await context.new_page()
        
        # Try to go to the dashboard directly
        print(f"Navigating to {DASHBOARD_URL}...")
        await page.goto(DASHBOARD_URL)
        
        # Check if we are redirected to login
        if "login" in page.url:
            print("Session expired or invalid. Please log in manually in the browser window.")
            await page.goto(LOGIN_URL)
            
            try:
                # Wait for user to reach the dashboard after manual login
                # 10-minute timeout for manual interaction
                await page.wait_for_url("**/homepage**", timeout=600000)
                print("Login detected! Saving new session state...")
            except Exception as e:
                print(f"Manual login timed out or failed: {e}")
                await browser.close()
                return
        else:
            print("Session is still valid! No manual login required.")

        # Save the current state (updated cookies/tokens)
        await context.storage_state(path=SESSION_FILE)
        print(f"Session state saved to {SESSION_FILE}")
        
        # Optional: Keep browser open for a moment to confirm
        await asyncio.sleep(2)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(manage_session())

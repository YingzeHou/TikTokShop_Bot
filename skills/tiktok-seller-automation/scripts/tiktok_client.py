import asyncio
import os
import json
from playwright.async_api import async_playwright, BrowserContext, Page
from playwright_stealth import Stealth

class TikTokSellerClient:
    def __init__(self, state_path: str, browser_profile: str):
        self.state_path = state_path
        self.browser_profile = browser_profile
        self.playwright = None
        self.browser_context = None
        self.page = None

    async def start(self, headless=True):
        self.playwright = await async_playwright().start()
        
        # Launching with persistent context to reuse session
        self.browser_context = await self.playwright.chromium.launch_persistent_context(
            self.browser_profile,
            headless=headless,
            channel="chrome",
            viewport={'width': 1920, 'height': 1080},
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        self.page = await self.browser_context.new_page()
        await Stealth().apply_stealth_async(self.page)
        return self.page

    async def navigate(self, url: str):
        print(f"Navigating to {url}...")
        await self.page.goto(url, wait_until="networkidle")
        await self.dismiss_overlays()

    async def dismiss_overlays(self):
        """Dismiss common onboarding popups."""
        try:
            # Check for "Got it" buttons
            buttons = ["Got it", "I understand", "Dismiss"]
            for btn_text in buttons:
                btn = self.page.get_by_text(btn_text, exact=False).first
                if await btn.is_visible():
                    print(f"Dismissing overlay: {btn_text}")
                    await btn.click()
                    await asyncio.sleep(1)
        except:
            pass

    async def scroll_to_bottom(self, steps=3, pause=1):
        """Scroll in increments to trigger lazy loading."""
        for i in range(steps):
            await self.page.evaluate(f"window.scrollBy(0, 800)")
            await asyncio.sleep(pause)

    async def get_clean_text(self):
        return await self.page.evaluate("document.body.innerText")

    async def stop(self):
        if self.browser_context:
            await self.browser_context.close()
        if self.playwright:
            await self.playwright.stop()

def clean_val(text: str):
    """Helper to clean currency and commas from strings."""
    if not text: return "0"
    return text.replace("$", "").replace(",", "").strip()

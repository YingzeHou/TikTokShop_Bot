import asyncio
import os
import json
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
        print(f"Fetching metrics from {target_url}...")
        await page.goto(target_url, wait_until="networkidle")
        
        # Dismiss initial overlays
        try:
            await page.get_by_text("Got it").click()
            await asyncio.sleep(1)
        except: pass

        # Wait for metrics to be visible
        print("Waiting for data cards to load...")
        # Search for common metric labels to confirm data is present
        await page.wait_for_selector("text=Gross Revenue", timeout=15000)
        
        # Scroll to ensure everything is rendered
        await page.evaluate("window.scrollTo(0, 400)")
        await asyncio.sleep(3)

        # Extraction Logic: Find cards and extract label + value pairs
        data = await page.evaluate("""() => {
            const results = {};
            
            // TikTok metrics often live in cards. We'll search for specific labels
            // and then find the adjacent value.
            const labels = ["Gross Revenue", "Orders", "Buyers", "Gross Revenue per Buyer", "SKU Views"];
            
            labels.forEach(label => {
                // Find the element containing the label text
                const el = Array.from(document.querySelectorAll('*')).find(e => 
                    e.childNodes.length === 1 && e.textContent.trim() === label
                );
                
                if (el) {
                    // Navigate up to the card container and find the value
                    // This is a heuristic: look for the largest number-like string nearby
                    const container = el.closest('div[class*="card"]') || el.parentElement.parentElement;
                    if (container) {
                        const valueEl = container.querySelector('[class*="value-content"]');
                        if (valueEl) {
                            results[label] = container.innerText.replace(label, '').trim().split('\\n')[0];
                        } else {
                            // Fallback: search all text in container for currency/number
                            results[label] = container.innerText;
                        }
                    }
                }
            });
            return results;
        }""")
        
        print("\n--- Extracted Metrics ---")
        for k, v in data.items():
            # Clean up the string (often contains 'VS previous period' etc)
            clean_val = v.split('\n')[0]
            print(f"{k}: {clean_val}")

        await context.close()

if __name__ == "__main__":
    asyncio.run(run())

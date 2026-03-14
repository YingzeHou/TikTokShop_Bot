import asyncio
import os
from tiktok_client import TikTokSellerClient

async def debug_layout(page):
    print("Capturing layout for debugging...")
    await page.evaluate("window.scrollTo(0, 1500)")
    await asyncio.sleep(5)
    
    # Save a new screenshot of exactly what's visible at this scroll position
    await page.screenshot(path="exploration/debug_scroll_1500.png")
    
    # List all iframes
    iframes = page.frames
    print(f"Detected {len(iframes)} frames on the page.")
    for idx, frame in enumerate(iframes):
        print(f"Frame {idx}: {frame.name} | URL: {frame.url[:100]}...")

    # Get the innerText of the specific area if possible
    content = await page.evaluate("document.body.innerText")
    with open("exploration/debug_text_1500.txt", "w") as f:
        f.write(content)
    
    print("✅ Debug data saved to exploration/debug_*")

async def run():
    client = TikTokSellerClient(
        state_path="session_state.json",
        browser_profile=os.path.join(os.getcwd(), "browser_profile")
    )
    await client.start(headless=True)
    await client.navigate("https://seller-us.tiktok.com/compass/data-overview?shop_region=US")
    await debug_layout(client.page)
    await client.stop()

if __name__ == "__main__":
    asyncio.run(run())

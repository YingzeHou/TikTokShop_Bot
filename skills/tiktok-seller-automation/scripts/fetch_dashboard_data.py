import asyncio
import os
import json
import re
from tiktok_client import TikTokSellerClient

def parse_overview(text: str):
    """Simple parser based on text dump format."""
    data = {}
    # Look for patterns like 'GMV\n$\n21,602\n.26'
    metrics = ["GMV", "Orders", "Customers", "Items sold", "AOV", "SKU orders", "LIVE GMV", "Product card GMV"]
    
    for metric in metrics:
        # Match label followed by some numbers/symbols
        pattern = rf"{metric}\n(.*?)(?=\n[A-Z]|$)"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            # Clean and combine the value parts
            raw_val = match.group(1).replace("\n", "").strip()
            data[metric] = raw_val
    return data

async def run_collection():
    client = TikTokSellerClient(
        state_path="session_state.json",
        browser_profile=os.path.join(os.getcwd(), "browser_profile")
    )
    
    await client.start(headless=True)
    
    # --- TASK 1: Overview Data ---
    overview_url = "https://seller-us.tiktok.com/compass/data-overview?shop_region=US"
    await client.navigate(overview_url)
    overview_text = await client.get_text_content()
    overview_data = parse_overview(overview_text)
    
    print("\n--- Summary: Compass Overview ---")
    print(json.dumps(overview_data, indent=2))
    
    # --- TASK 2: Explore Product Analytics (Mapping phase) ---
    product_url = "https://seller-us.tiktok.com/compass/product-analytics?shop_region=US"
    print(f"\nMoving to {product_url} for mapping...")
    await client.navigate(product_url)
    
    # Capture mapping data for next steps
    product_text = await client.get_text_content()
    os.makedirs("exploration", exist_ok=True)
    with open("exploration/product_analytics_dump.txt", "w") as f:
        f.write(product_text)
    
    await client.page.screenshot(path="exploration/product_analytics.png", full_page=True)
    print("✅ Product Analytics mapped to exploration/ folder.")

    # Save final report
    report = {
        "overview": overview_data,
        "timestamp": "2026-03-13" # Or dynamic
    }
    with open("daily_report.json", "w") as f:
        json.dump(report, f, indent=2)

    await client.stop()

if __name__ == "__main__":
    asyncio.run(run_collection())

import asyncio
import os
import json
import re
from tiktok_client import TikTokSellerClient

def parse_breakdown_from_text(text: str):
    """
    Parses GMV breakdown from raw page text.
    Format found in debug dump:
    LIVE\nView analysis\n$463.01\n20.56%
    Videos\nView analysis\n$12,217.30\n28.2%
    """
    results = {}
    categories = ["LIVE", "Videos", "Product card"]
    
    for cat in categories:
        # Match Category name, then optional 'View analysis', then Value, then Percentage
        # This handles the exact format we saw in the debug_text_1500.txt
        pattern = rf"{cat}.*?\n(?:View analysis\n)?(\$[\d,.]+)\n([\d.]+%?)"
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            results[cat] = {
                "value": match.group(1),
                "percentage": match.group(2),
                "subs": {}
            }
            # Heuristic for sub-sections: look for the text immediately following until the next major category
            # This is complex in regex, so we'll do a simple substring scan for "Affiliate" or "Linked" 
            # within a small window after the category
            window = text[match.end():match.end()+500]
            for sub in ["Affiliate accounts", "Linked accounts"]:
                sub_pattern = rf"{sub}\n(\$[\d,.]+)\n([\d.]+%?)"
                sub_match = re.search(sub_pattern, window)
                if sub_match:
                    results[cat]["subs"][sub] = {
                        "value": sub_match.group(1),
                        "percentage": sub_match.group(2)
                    }
                    
    return results

async def run():
    client = TikTokSellerClient(
        state_path="session_state.json",
        browser_profile=os.path.join(os.getcwd(), "browser_profile")
    )
    await client.start(headless=True)
    await client.navigate("https://seller-us.tiktok.com/compass/data-overview?shop_region=US")
    
    # 1. Scroll and Wait
    print("Scrolling to breakdown area...")
    await client.page.evaluate("window.scrollTo(0, 1800)")
    await asyncio.sleep(5)
    
    # 2. Extract Sub-breakdowns by clicking
    # We'll try to click all expand icons on the page to populate the text
    try:
        expanders = await client.page.query_selector_all(".arco-table-cell-expand-icon")
        print(f"Clicking {len(expanders)} expanders...")
        for exp in expanders:
            await exp.click()
            await asyncio.sleep(1)
    except: pass

    # 3. Get the text after all expansions
    print("Capturing expanded text...")
    full_text = await client.page.evaluate("document.body.innerText")
    
    # 4. Parse
    final_data = parse_breakdown_from_text(full_text)
    
    print("\n--- DETAILED GMV REPORT (TEXT-PARSED) ---")
    print(json.dumps(final_data, indent=2))
    
    with open("detailed_gmv_breakdown.json", "w") as f:
        json.dump(final_data, f, indent=2)

    await client.stop()

if __name__ == "__main__":
    asyncio.run(run())

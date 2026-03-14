import asyncio
import os
import json
import re
from tiktok_client import TikTokSellerClient, clean_val

async def scrape_compass_overview(client: TikTokSellerClient, for_today=False):
    url = "https://seller-us.tiktok.com/compass/data-overview?shop_region=US"
    if for_today:
        url += "&date_type=1"
        
    print(f"\n[Compass Overview] Navigating to {'Today' if for_today else 'Default'}...")
    await client.navigate(url)
    await asyncio.sleep(5)
    
    # 1. Expand breakdowns (Affiliate/Linked)
    print("Expanding breakdowns...")
    try:
        expanders = await client.page.query_selector_all(".arco-table-cell-expand-icon")
        for exp in expanders:
            if await exp.is_visible():
                await exp.click()
                await asyncio.sleep(1)
    except: pass
    
    text = await client.get_clean_text()
    
    # --- Key Metrics Parser (Anchored to 'Key metrics' section) ---
    metrics = {}
    # Find the start of the metrics section to avoid sidebar links
    metrics_section_match = re.search(r"Key metrics.*?(?=GMV)", text, re.DOTALL)
    if metrics_section_match:
        metrics_text = text[metrics_section_match.start():]
    else:
        metrics_text = text # Fallback

    keys = ["GMV", "Orders", "Customers", "Items sold", "AOV", "SKU orders", "LIVE GMV", "Product card GMV"]
    for key in keys:
        # Match the key, then skip any whitespace/symbols, then grab the number
        # Pattern: Label -> optional '$' -> digits/commas -> optional decimals
        pattern = rf"{key}\s*\n\s*(\$?\s*[\d,]+(?:\s*\.\d+)?)"
        match = re.search(pattern, metrics_text, re.MULTILINE)
        if match:
            val = match.group(1).replace("\n", "").replace(" ", "").strip()
            metrics[key] = val
            
    # --- Detailed Breakdown Parser ---

    breakdown = {}
    for cat in ["LIVE", "Videos", "Product card"]:
        pattern = rf"{cat}.*?\n(?:View analysis\n)?(\$[\d,.]+)\n([\d.]+%?)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            entry = {"value": match.group(1), "percentage": match.group(2), "subs": {}}
            # Window check for sub-breakdowns (Affiliate/Linked)
            window = text[match.end():match.end()+500]
            for sub in ["Affiliate accounts", "Linked accounts"]:
                sub_pattern = rf"{sub}\n(\$[\d,.]+)\n([\d.]+%?)"
                sub_match = re.search(sub_pattern, window)
                if sub_match:
                    entry["subs"][sub] = {"value": sub_match.group(1), "percentage": sub_match.group(2)}
            breakdown[cat] = entry
            
    return {"key_metrics": metrics, "gmv_breakdown": breakdown}

async def scrape_product_analytics(client: TikTokSellerClient):
    print("\n[Product Analytics] Navigating...")
    try:
        # SPA Navigation via sidebar
        await client.page.get_by_text("Product analytics", exact=True).click()
        await asyncio.sleep(15) # Wait for data cards
        await client.scroll_to_bottom(steps=2)
    except Exception as e:
        print(f"Product Analytics Click Failed: {e}")
        return {}

    text = await client.get_clean_text()
    
    # --- Product Ranking Parser ---
    ranking = []
    # Find all product patterns: Name\nID: xxx\nType\nValue\nOrders\nUnits
    # Example: Name, ID, Source, Value, Orders, Units
    product_pattern = re.compile(r"ID: (\d+)\n\n(.*?)\n\n(\$[\d,.]+)\n\n(\d+)\n\n(\d+)", re.MULTILINE)
    
    # This matches the structure we found: 
    # [Name before ID]\nID: [ID]\n\n[Source]\n\n[Value]\n\n[Orders]\n\n[Units]
    # Let's use a simpler iterative line parser based on ID: 
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if "ID: " in line:
            try:
                # Name is usually 1 line above
                name = lines[i-1]
                id_val = line.split(": ")[1].strip()
                source = lines[i+2]
                value = lines[i+4]
                orders = lines[i+6]
                units = lines[i+8]
                
                ranking.append({
                    "name": name,
                    "id": id_val,
                    "source": source,
                    "value": value,
                    "orders": orders,
                    "units": units
                })
            except: continue

    return {"product_ranking": ranking[:10]} # Return top 10

async def main():
    client = TikTokSellerClient(
        state_path="session_state.json",
        browser_profile=os.path.join(os.getcwd(), "browser_profile")
    )
    
    # Check if we want today's data
    for_today = os.getenv("TIKTOK_REPORT_TODAY", "false").lower() == "true"
    
    try:
        await client.start(headless=True)
        
        overview = await scrape_compass_overview(client, for_today=for_today)
        products = await scrape_product_analytics(client)
        
        final_report = {
            "overview": overview,
            "product_ranking": products,
            "timestamp": "2026-03-13" 
        }
        
        report_path = "tiktok_daily_report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(final_report, f, indent=2)
        
        print(f"\n✅ REPORT GENERATED: {os.path.abspath(report_path)}")
        
    finally:
        await client.stop()

if __name__ == "__main__":
    asyncio.run(main())

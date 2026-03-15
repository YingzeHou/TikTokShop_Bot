import sys
import os
import json
# Add project root to sys.path
sys.path.append(os.getcwd())

from skills.tiktok_seller_automation.scripts.tiktok_api_client import TikTokApiClient
from skills.tiktok_seller_automation.scripts.endpoint_builder import EndpointBuilder

def run_report():
    # Initialize client
    client = TikTokApiClient()
    builder = EndpointBuilder()
    
    # Get dates
    start, end = builder.get_default_dates()
    print(f"Running report for {start} to {end}...")
    
    # Build payload for Page 0
    payload = builder.build_product_subscription_payload(start, end, page=0)
    
    # Call API
    response = client.call_api('product_subscriptions', payload=payload)
    
    if response.get("code") == 0:
        data = response.get("data", {})
        stats = data.get("stats", [])
        print(f"\nSuccess! Found {len(stats)} products on page 0.")
        
        for p in stats:
            name = p.get('product_name', 'N/A')
            subs = p.get('active_subscriptions', 0)
            gmv = p.get('subscription_gmv', {}).get('amount_formatted', '$0.00')
            print(f"- {name[:60]}... | Subs: {subs} | GMV: {gmv}")
            
        pagination = data.get("list_control", {}).get("next_pagination", {})
        print(f"\nPagination: {pagination}")
    else:
        print(f"Error in API call: {response.get('message')}")

if __name__ == "__main__":
    run_report()

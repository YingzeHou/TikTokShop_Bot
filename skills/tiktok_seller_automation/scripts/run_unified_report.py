import sys
import os
import json
from datetime import datetime
# Add project root to sys.path
sys.path.append(os.getcwd())

from skills.tiktok_seller_automation.scripts.tiktok_api_client import TikTokApiClient
from skills.tiktok_seller_automation.scripts.endpoint_builder import EndpointBuilder
from skills.tiktok_seller_automation.scripts.data_fetcher import DataFetcher

def run_unified_report(start_date=None, end_date=None):
    # Initialize components
    client = TikTokApiClient()
    builder = EndpointBuilder()
    fetcher = DataFetcher(client)
    
    # Define report parameters
    if start_date and end_date:
        start, end = start_date, end_date
    else:
        start, end = builder.get_default_dates()
    
    print(f"=== Unified Report for {start} to {end} ===\n")
    
    report_sections = {}
    
    # Section 1: Product Subscriptions
    print("Section 1: Fetching Product Subscriptions...")
    report_sections['subscription_data'] = fetcher.fetch_all_pages(
        endpoint_key='product_subscriptions', 
        payload_builder_func=builder.build_product_subscription_payload,
        start_date=start, 
        end_date=end
    )
    
    # Section 2: Campaign List
    print("\nSection 2: Fetching Campaign List...")
    report_sections['campaign_data'] = fetcher.fetch_all_pages(
        endpoint_key='campaign_list',
        payload_builder_func=builder.build_campaign_list_payload,
        start_date=start,
        end_date=end
    )
    
    # Section 3: General Product Performance
    print("\nSection 3: Fetching General Product Performance...")
    report_sections['product_performance_general'] = fetcher.fetch_all_pages(
        endpoint_key='product_performance_general',
        payload_builder_func=builder.build_product_performance_general_payload,
        start_date=start,
        end_date=end
    )
    
    # Section 4: Product Performance List (Iterate through campaigns)
    print("\nSection 4: Fetching Product Performance per Campaign...")
    all_product_performance = []
    for campaign in report_sections.get('campaign_data', []):
        camp_id = campaign.get('campaign_id')
        camp_name = campaign.get('campaign_name')
        if camp_id:
            print(f"  Fetching products for campaign: {camp_name} ({camp_id})...")
            camp_products = fetcher.fetch_all_pages(
                endpoint_key='product_list',
                payload_builder_func=builder.build_product_list_payload,
                start_date=start,
                end_date=end,
                campaign_id=camp_id
            )
            # Add campaign info to each product record
            for p in camp_products:
                p['parent_campaign_id'] = camp_id
                p['parent_campaign_name'] = camp_name
            all_product_performance.extend(camp_products)
    
    report_sections['product_performance_data'] = all_product_performance
    
    # Metadata
    metadata = {
        "start_date": start,
        "end_date": end,
        "generated_at": datetime.now().isoformat(),
        "seller_id": client.config['oec_seller_id']
    }
    
    # Save unified report
    report_file = f"unified_report_{start}.json"
    unified_report = {
        "metadata": metadata,
        "sections": report_sections
    }
    
    with open(report_file, "w") as f:
        json.dump(unified_report, f, indent=4)
    
    print(f"\n{'='*40}")
    print(f"Unified Report generated: {report_file}")
    for section, data in report_sections.items():
        print(f"- {section}: {len(data)} items")
    print(f"{'='*40}")

if __name__ == "__main__":
    s = sys.argv[1] if len(sys.argv) > 1 else None
    e = sys.argv[2] if len(sys.argv) > 2 else None
    run_unified_report(s, e)

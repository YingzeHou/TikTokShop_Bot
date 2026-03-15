import sys
import os
import json
# Add project root to sys.path
sys.path.append(os.getcwd())

from skills.tiktok_seller_automation.scripts.tiktok_api_client import TikTokApiClient
from skills.tiktok_seller_automation.scripts.endpoint_builder import EndpointBuilder
from skills.tiktok_seller_automation.scripts.data_fetcher import DataFetcher

def run_report():
    # Initialize components
    client = TikTokApiClient()
    builder = EndpointBuilder()
    fetcher = DataFetcher(client)
    
    # Define report parameters
    start, end = builder.get_default_dates()
    print(f"Running report for {start} to {end}...")
    
    # 1. Fetch data using the generic fetcher
    all_data = fetcher.fetch_all_pages(
        endpoint_key='product_subscriptions', 
        payload_builder_func=builder.build_product_subscription_payload,
        start_date=start, 
        end_date=end
    )
    
    # 2. Save report using the generic saver
    report_file = fetcher.save_report(
        data=all_data, 
        report_name="subscriptions", 
        metadata={"start_date": start, "end_date": end}
    )
    
    print(f"\nFinal report: {report_file}")
    print(f"Total items fetched: {len(all_data)}")

if __name__ == "__main__":
    run_report()

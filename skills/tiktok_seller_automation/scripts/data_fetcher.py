import json
from datetime import datetime

class DataFetcher:
    def __init__(self, api_client):
        self.client = api_client

    def fetch_all_pages(self, endpoint_key, payload_builder_func, **builder_kwargs):
        """
        Generic multi-page fetcher.
        :param endpoint_key: Key in config.yaml endpoints.
        :param payload_builder_func: Function that takes page, size, etc. and returns a payload.
        :param builder_kwargs: Arguments for the payload builder (e.g. start_date, end_date).
        """
        all_data = []
        page = 0
        has_more = True
        
        while has_more:
            print(f"Fetching {endpoint_key} page {page}...")
            # Build payload with current pagination
            payload = payload_builder_func(page=page, **builder_kwargs)
            
            try:
                response = self.client.call_api(endpoint_key, payload=payload)
                
                if response.get("code") == 0:
                    data = response.get("data", {})
                    # Note: stats is specific to the current endpoint; 
                    # for future APIs, we might need to make this key configurable.
                    items = data.get("stats", []) 
                    all_data.extend(items)
                    
                    pagination = data.get("list_control", {}).get("next_pagination", {})
                    has_more = pagination.get("has_more", False)
                    page = pagination.get("next_page", page + 1)
                    
                    print(f"  Retrieved {len(items)} items. Total: {len(all_data)}")
                else:
                    print(f"  API Error: {response.get('message')}")
                    break
            except Exception as e:
                print(f"  Request failed: {e}")
                break
                
        return all_data

    def save_report(self, data, report_name, metadata=None):
        """
        Saves fetched data into a structured JSON report.
        """
        report_file = f"report_{report_name}_{datetime.now().strftime('%Y-%m-%d')}.json"
        report_data = {
            "report_info": {
                "report_type": report_name,
                "total_items": len(data),
                "generated_at": datetime.now().isoformat(),
                **(metadata or {})
            },
            "data": data
        }
        
        with open(report_file, "w") as f:
            json.dump(report_data, f, indent=4)
            
        print(f"\nReport saved to: {report_file}")
        return report_file

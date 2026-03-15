import json
from datetime import datetime

class DataFetcher:
    def __init__(self, api_client):
        self.client = api_client

    def fetch_all_pages(self, endpoint_key, payload_builder_func, **builder_kwargs):
        """
        Generic multi-page fetcher.
        """
        endpoint_info = self.client.config['endpoints'].get(endpoint_key)
        data_key = endpoint_info.get('data_key', 'stats')
        pagination_type = endpoint_info.get('pagination_type', 'list_control')
        
        all_data = []
        # Page starts at 0 for list_control, 1 for page_count/page_number
        page = 1 if pagination_type in ["page_number", "page_count"] else 0
        has_more = True
        
        while has_more:
            print(f"Fetching {endpoint_key} page {page}...")
            payload = payload_builder_func(page=page, **builder_kwargs)
            
            try:
                response = self.client.call_api(endpoint_key, payload=payload)
                if response.get("code") == 0:
                    data = response.get("data", {})
                    items = data.get(data_key, [])
                    if isinstance(items, list):
                        all_data.extend(items)
                    elif isinstance(items, dict):
                        all_data.append(items) # For single objects

                    # Handle pagination detection
                    if pagination_type == "list_control":
                        pagination = data.get("list_control", {}).get("next_pagination", {})
                        has_more = pagination.get("has_more", False)
                        page = pagination.get("next_page", page + 1)
                    elif pagination_type == "page_count":
                        pagination = data.get("pagination", {})
                        total_page = pagination.get("page_count", 1)
                        has_more = page < total_page
                        page += 1
                    elif pagination_type == "page_number":
                        page_size = payload.get("page_size", 10)
                        has_more = len(items) == page_size
                        page += 1
                    else:
                        has_more = False # No pagination

                    print(f"  Retrieved {len(items) if isinstance(items, list) else 1} items. Total: {len(all_data)}")
                else:
                    msg = response.get('msg') or response.get('message') or "Unknown Error"
                    print(f"  API Error: {msg}")
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

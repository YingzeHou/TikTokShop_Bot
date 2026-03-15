import json
import os
import requests

SESSION_FILE = "session_state.json"
API_URL = "https://seller-us.tiktok.com/api/v2/insights/seller/ttp/product/product_subscription/products/list"

def get_cookies_from_state(state_file):
    if not os.path.exists(state_file):
        raise FileNotFoundError(f"Session file {state_file} not found. Run session_manager.py first.")
    
    with open(state_file, 'r') as f:
        state = json.load(f)
    
    # Playwright's storage state has a 'cookies' list
    cookies = state.get('cookies', [])
    cookie_dict = {c['name']: c['value'] for c in cookies}
    return cookie_dict

def test_subscription_api():
    try:
        cookies = get_cookies_from_state(SESSION_FILE)
        
        # Build common query parameters
        params = {
            "locale": "en",
            "language": "en",
            "oec_seller_id": "7495613311299782811",
            "aid": "4068",
            "app_name": "i18n_ecom_shop",
            "device_platform": "web",
            "cookie_enabled": "true",
            "browser_language": "en-US",
            "browser_platform": "MacIntel",
            "browser_name": "Mozilla",
            "timezone_name": "America/Los_Angeles",
            "use_content_type_definition": "1"
        }
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            "Referer": "https://seller-us.tiktok.com/homepage",
            "Origin": "https://seller-us.tiktok.com"
        }

        def fetch_page(page_number):
            payload = {
                "request": {
                    "time_descriptor": {"start": "2026-03-08", "end": "2026-03-15"},
                    "filter": {},
                    "list_control": {
                        "pagination": {"page": page_number, "size": 10},
                        "rules": [{"direction": 2, "field": "active_subscriptions"}]
                    }
                }
            }
            print(f"--- Fetching Page {page_number} ---")
            response = requests.post(API_URL, params=params, json=payload, headers=headers, cookies=cookies)
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0:
                    stats = data.get("data", {}).get("stats", [])
                    print(f"Success! Retrieved {len(stats)} products.")
                    if stats:
                        print(f"First product on page {page_number}: {stats[0].get('product_name')[:50]}...")
                    
                    pagination = data.get("data", {}).get("list_control", {}).get("next_pagination", {})
                    print(f"Pagination info: {pagination}")
                    return stats, pagination
                else:
                    print(f"API Error: {data.get('message')}")
            else:
                print(f"HTTP Error: {response.status_code}")
            return None, None

        # Fetch Page 0
        stats0, pag0 = fetch_page(0)
        
        # Fetch Page 1 if more results exist
        if pag0 and pag0.get("has_more"):
            stats1, pag1 = fetch_page(1)
            
            if stats0 and stats1:
                # Basic check to see if we actually got different products
                if stats0[0].get("product_id") != stats1[0].get("product_id"):
                    print("\nPagination Validated: Page 1 results are different from Page 0.")
                else:
                    print("\nWarning: Page 1 results seem identical to Page 0.")
        else:
            print("\nNo more pages to fetch.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_subscription_api()

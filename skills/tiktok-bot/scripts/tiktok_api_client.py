import requests
import json
import os
import sys

# Add current directory to path for imports
curr_dir = os.path.dirname(os.path.abspath(__file__))
if curr_dir not in sys.path:
    sys.path.append(curr_dir)

from utils import load_config, get_cookies_from_state

class TikTokApiClient:
    def __init__(self, config_path=None):
        self.config = load_config(config_path)
        self.base_url = self.config['base_url']
        self.session_file = self.config['session_file']
        self.session = requests.Session()
        # Initial headers from config
        self.session.headers.update(self.config['default_headers'])
        
        # Cache for domain cookies to avoid re-reading the file too often
        self._cookie_cache = {}

    def _load_domain_session(self, domain_key):
        """Loads and updates session with cookies for a specific domain key."""
        if domain_key not in self._cookie_cache:
            try:
                cookies = get_cookies_from_state(self.session_file, domain_key)
                self._cookie_cache[domain_key] = cookies
            except Exception as e:
                print(f"Warning: Could not load cookies for {domain_key}: {e}")
                return
        
        # Clear current cookies and update with domain-specific ones
        self.session.cookies.clear()
        self.session.cookies.update(self._cookie_cache[domain_key])

    def _build_params(self, extra_params=None):
        params = self.config['default_params'].copy()
        params['oec_seller_id'] = self.config['oec_seller_id']
        params['aadvid'] = self.config['aadvid']
        params['bc_id'] = self.config['bc_id']
        if extra_params:
            params.update(extra_params)
        return params

    def call_api(self, endpoint_key, extra_params=None, payload=None):
        endpoint_info = self.config['endpoints'].get(endpoint_key)
        if not endpoint_info:
            raise ValueError(f"Endpoint '{endpoint_key}' not defined in config.")
        
        # 1. Determine URL
        url = endpoint_info.get('url') or f"{self.base_url}{endpoint_info['path']}"
            
        # 2. Determine domain and load corresponding session state
        is_ads = "ads.tiktok.com" in url
        domain_key = "ads_center" if is_ads else "seller_center"
        self._load_domain_session(domain_key)

        # 3. Update headers
        if is_ads:
            self.session.headers.update({
                "Origin": "https://ads.tiktok.com",
                "Referer": "https://ads.tiktok.com/"
            })
        else:
            self.session.headers.update({
                "Origin": "https://seller-us.tiktok.com",
                "Referer": "https://seller-us.tiktok.com/homepage"
            })

        method = endpoint_info['method']
        params = self._build_params(extra_params)
        
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=payload
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            response.raise_for_status()

# For local testing, let's fix the import path issue
if __name__ == "__main__":
    import sys
    import os
    # Add project root to sys.path to allow imports to work when run directly
    sys.path.append(os.getcwd())
    
    # Simple test
    client = TikTokApiClient()
    print("TikTok API Client initialized successfully.")

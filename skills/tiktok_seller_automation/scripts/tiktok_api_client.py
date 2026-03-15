import requests
import json
from skills.tiktok_seller_automation.scripts.utils import load_config, get_cookies_from_state

class TikTokApiClient:
    def __init__(self, config_path="skills/tiktok_seller_automation/scripts/config.yaml"):
        self.config = load_config(config_path)
        self.base_url = self.config['base_url']
        self.seller_id = self.config['oec_seller_id']
        self.session_file = self.config['session_file']
        
        # Load cookies
        self.cookies = get_cookies_from_state(self.session_file)
        
        # Initialize session
        self.session = requests.Session()
        self.session.cookies.update(self.cookies)
        self.session.headers.update(self.config['default_headers'])

    def _build_params(self, extra_params=None):
        params = self.config['default_params'].copy()
        params['oec_seller_id'] = self.seller_id
        if extra_params:
            params.update(extra_params)
        return params

    def call_api(self, endpoint_key, extra_params=None, payload=None):
        endpoint_info = self.config['endpoints'].get(endpoint_key)
        if not endpoint_info:
            raise ValueError(f"Endpoint '{endpoint_key}' not defined in config.")
        
        url = f"{self.base_url}{endpoint_info['path']}"
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

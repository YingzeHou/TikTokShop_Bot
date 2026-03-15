import yaml
import json
import os

def load_config(config_path="skills/tiktok_seller_automation/scripts/config.yaml"):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_cookies_from_state(state_file):
    if not os.path.exists(state_file):
        raise FileNotFoundError(f"Session file {state_file} not found. Run session_manager.py first.")
    
    with open(state_file, 'r') as f:
        state = json.load(f)
    
    cookies = state.get('cookies', [])
    return {c['name']: c['value'] for c in cookies}

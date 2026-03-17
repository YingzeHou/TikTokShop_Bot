import yaml
import json
import os

def load_config(config_path=None):
    if not config_path:
        # Default to config.yaml in the same directory as the script
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yaml")
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_cookies_from_state(state_file, domain_key="seller_center"):
    """
    Extracts cookies from a mapped session state file.
    Expected format: { "domain_key": { "cookies": [...], "origins": [...] } }
    """
    if not os.path.exists(state_file):
        raise FileNotFoundError(f"Session file {state_file} not found. Run session_manager.py first.")
    
    with open(state_file, 'r') as f:
        full_state = json.load(f)
    
    # Check if the file is using the new mapping format or the old flat format
    if domain_key in full_state:
        state = full_state[domain_key]
    else:
        # Fallback to the whole file if the key isn't found (for backward compatibility)
        state = full_state

    cookies = state.get('cookies', [])
    return {c['name']: c['value'] for c in cookies}

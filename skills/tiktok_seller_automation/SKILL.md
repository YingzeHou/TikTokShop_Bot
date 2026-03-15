---
name: tiktok_seller_automation
description: Modular and robust automation for TikTok Shop Seller Center.
---

# TikTok Shop Seller Automation Skill (Modular)

This skill provides a modular and robust architecture for automating data retrieval from the TikTok Shop Seller Center. It replaces the old, monolithic approach with a clean Separation of Concerns (SoC) using:
- **Playwright** for interactive and automated session management.
- **TikTokApiClient** for session-persistent API communication.
- **EndpointBuilder** for structured JSON request payloads.
- **Centralized YAML** for configuration and maintenance.

## Folder Structure
- `scripts/session_manager.py`: Handles interactive login and saves `session_state.json`.
- `scripts/tiktok_api_client.py`: Core client for making authenticated API requests.
- `scripts/endpoint_builder.py`: Constructs JSON payloads for various endpoints.
- `scripts/config.yaml`: Centralized configuration for URLs, headers, and endpoints.
- `scripts/run_report.py`: High-level script to fetch and display subscription reports.

## Workflows

### 1. Initialize/Refresh Session
If the session is expired or missing, run this to log in interactively.
- **Command**: `venv/bin/python3 skills/tiktok_seller_automation/scripts/session_manager.py`

### 2. Run Subscription Report
Fetches the latest product subscription data and GMV.
- **Command**: `venv/bin/python3 skills/tiktok_seller_automation/scripts/run_report.py`

## Configuration
Update `skills/tiktok_seller_automation/scripts/config.yaml` to change:
- `oec_seller_id`: Your TikTok Shop Seller ID.
- `base_url`: The Seller Center base URL.
- Endpoints and default parameters.

## Implementation Details
- **Authentication**: Uses Playwright's `storage_state` (cookies + local storage) saved in `session_state.json`.
- **API Communication**: Uses the `requests` library with session persistence.
- **Modularity**: Clean separation between API logic (`tiktok_api_client.py`) and request building (`endpoint_builder.py`).

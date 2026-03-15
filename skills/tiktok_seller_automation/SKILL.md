---
name: tiktok_seller_automation
description: Modular and robust automation for TikTok Shop Seller Center and Ads APIs.
---

# TikTok Shop Seller Automation Skill (Unified MVP)

This skill provides a modular and robust architecture for automating data retrieval from the TikTok Shop Seller Center and TikTok Ads APIs. It features:
- **Multi-Domain Session Management**: Captures and maps session states for both `seller-us.tiktok.com` and `ads.tiktok.com`.
- **Unified Reporting**: Consolidates product subscriptions, campaign statistics, and product performance into a single JSON report.
- **Separation of Concerns**: Clean architecture with dedicated classes for API communication, request building, and data fetching.

## Folder Structure
- `scripts/session_manager.py`: Interactive login tool to capture mapped `session_state.json`.
- `scripts/tiktok_api_client.py`: Core client that handles domain-specific sessions and headers.
- `scripts/endpoint_builder.py`: Constructs JSON payloads for all supported endpoints.
- `scripts/data_fetcher.py`: Generic multi-page fetcher supporting various pagination styles.
- `scripts/run_unified_report.py`: Orchestrator for the unified data extraction workflow.
- `scripts/config.yaml`: Centralized configuration for URLs, headers, and endpoints.
- `scripts/utils.py`: Shared utilities for config and session state handling.

## Workflows

### 1. Initialize/Refresh Sessions
Run this to capture separate sessions for Seller Center and Ads Center.
- **Command**: `venv/bin/python3 skills/tiktok_seller_automation/scripts/session_manager.py`
- **Action**: Follow the prompts to log in via the browser and press Enter in the terminal to capture each state.

### 2. Generate Unified Report
Fetches all data and generates a consolidated JSON report.
- **Command**: `venv/bin/python3 skills/tiktok_seller_automation/scripts/run_unified_report.py`
- **Output**: `unified_report_YYYY-MM-DD.json` containing `subscription_data`, `campaign_data`, and `product_performance_data`.

## Configuration
Update `skills/tiktok_seller_automation/scripts/config.yaml` to change:
- `oec_seller_id`: Your TikTok Shop Seller ID.
- `aadvid`: Your TikTok Ads Advertiser ID.
- `bc_id`: Your Business Center ID.
- Endpoints and pagination settings.

## Implementation Details
- **Authentication**: Mapped JSON in `session_state.json` stores `{ "seller_center": {...}, "ads_center": {...} }`.
- **Dynamic Headers**: The client automatically updates `Origin` and `Referer` headers based on the target domain.
- **Pagination Support**: Handles `list_control`, `page_count`, and `page_number` styles.

---
name: tiktok-seller-automation
description: Automates data retrieval and reporting from the TikTok Shop Seller Center using Playwright. Use this skill when you need to extract sales, order, or finance data from the seller dashboard while handling session persistence.
---

# TikTok Seller Automation

## Overview

This skill provides a modular suite of tools to automate data retrieval from the TikTok Shop Seller Center. It utilizes a shared `TikTokSellerClient` for session management and stealthy navigation, allowing for efficient multi-tab data collection in a single browser session.

## Workflow: Session Management

1. **Initial Login**: Run `scripts/auth_session.py`. This opens a headed browser for manual login and 2FA.
2. **Session Storage**: Cookies and local storage are saved to `session_state.json`.
3. **Persistent Profile**: A `browser_profile/` directory is maintained to look like a "real" browser and avoid bot detection.

## Core Capabilities

### 1. Automated Daily Reporting
- **Script**: `scripts/generate_tiktok_report.py`
- **Output**: `tiktok_daily_report.json`
- **Data Captured**:
    - **Key Metrics**: GMV, Orders, Customers, Items sold, AOV, SKU orders.
    - **GMV Breakdown**: LIVE, Videos, Product Card (Value & Percentage).
    - **Sub-Breakdowns**: Affiliate vs. Linked accounts (requires expandable row logic).
    - **Product Ranking**: Top 10 SKUs with GMV, Orders, and Units.

### 2. Modular Scraper Development
- **Utility**: `scripts/tiktok_client.py` provides the `TikTokSellerClient` class.
- **Exploration**: Use `scripts/dump_text.py` or `scripts/debug_layout.py` to map new sections of the dashboard.

## Resources

### scripts/
- `tiktok_client.py`: Shared browser logic, stealth application, and common UI interactions.
- `auth_session.py`: Utility for manual login and session capture.
- `generate_tiktok_report.py`: The primary orchestrator for daily data collection.
- `fetch_detailed_breakdown.py`: Specialized script for GMV breakdown analysis.

### references/
- Logic for parsing raw page text into structured JSON metrics.

---

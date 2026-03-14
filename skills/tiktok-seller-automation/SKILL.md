---
name: tiktok-seller-automation
description: Automates data retrieval and reporting from the TikTok Shop Seller Center. Use this skill when the user wants to login, capture sessions, or retrieve daily sales and product metrics.
---

# TikTok Seller Automation

## 🛠 Direct Action Guide

Follow these instructions strictly. Do NOT create new exploration or probe scripts. Use the established tools in `scripts/`.

### 1. Manual Login & Session Capture
**Trigger**: When the user needs to log in for the first time or if the session expires.
- **Action**: Run the authentication script.
- **Command**: `python3 skills/tiktok-seller-automation/scripts/auth_session.py`
- **Instruction**: Follow terminal prompts to manually log in and press Enter.

### 2. Retrieve Daily Report (Yesterday)
**Trigger**: When the user asks for a daily report, sales data, or "yesterday's" data.
- **Action**: Run the report generator (defaults to yesterday).
- **Environment**: Set `PYTHONPATH` to include the `scripts` directory.
- **Command**: `PYTHONPATH=skills/tiktok-seller-automation/scripts python3 skills/tiktok-seller-automation/scripts/generate_tiktok_report.py`
- **Output**: The report is saved to `tiktok_daily_report.json`.

### 3. Retrieve Today's Data
**Trigger**: When the user specifically asks for "Today's" data or "real-time" metrics.
- **Action**: Run the report generator with the `TIKTOK_REPORT_TODAY` flag.
- **Command**: `TIKTOK_REPORT_TODAY=true PYTHONPATH=skills/tiktok-seller-automation/scripts python3 skills/tiktok-seller-automation/scripts/generate_tiktok_report.py`

## 📂 Resources
- `tiktok_client.py`: Shared browser and stealth logic.
- `auth_session.py`: Headed browser login tool.
- `generate_tiktok_report.py`: Main data extraction orchestrator.

---

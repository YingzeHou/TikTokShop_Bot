---
name: tiktok-seller-automation
description: Automates data retrieval and reporting from the TikTok Shop Seller Center using Playwright. Use this skill when you need to extract sales, order, or finance data from the seller dashboard while handling session persistence.
---

# TikTok Seller Automation

## Overview

This skill provides a suite of tools and workflows to automate repetitive data retrieval tasks from the TikTok Shop Seller Center. It uses Playwright to navigate the dashboard and can reuse authenticated sessions to bypass 2FA once initially logged in.

## Workflow: Session Management

Before any automation can run, a valid session must be captured.

1. **Initial Login**: Run `scripts/auth_session.py`. This opens a browser window for you to manually log in and handle 2FA.
2. **Session Storage**: The script saves your cookies and local storage to `session_state.json`.
3. **Automated Re-use**: Subsequent scripts will load `session_state.json` to perform tasks without requiring manual login.

## Capabilities

### 1. Session Capture
- **Script**: `scripts/auth_session.py`
- **Usage**: Use this when the session expires or for the first-time setup.

### 2. Exploration & Mapping (Coming Soon)
- Capture screenshots and HTML of specific dashboard sections to identify data selectors.

### 3. Data Retrieval (Coming Soon)
- Exporting Daily Sales reports.
- Extracting Order history.
- Downloading Finance/Settlement statements.

## Resources

### scripts/
- `auth_session.py`: Launches a headed browser for manual login and saves the session state.

### references/
- [TODO] Add data schemas and selector maps here as we explore.

---


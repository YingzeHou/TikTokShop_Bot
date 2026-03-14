# TikTok Shop Seller Center Automation

A modular, Playwright-based automation suite for retrieving daily reports, metrics, and product performance from the TikTok Shop Seller Center.

## 🚀 Quick Start (Deployment)

### 1. Environment Setup
Ensure you have **Python 3.12** installed.

```bash
# Clone the repository
git clone <your-repo-url>
cd TikTokShop_Bot

# Create and activate virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. One-Time Authentication
Run the session capture script to log in manually. This will save your session state so automation can bypass 2FA in the future.

```bash
python skills/tiktok-seller-automation/scripts/auth_session.py
```
*Follow the instructions in the browser window to log in. Once you see the dashboard, return to the terminal and press Enter.*

### 3. Generate Daily Report
Run the master collector to fetch Overview metrics, GMV breakdowns, and Product rankings.

```bash
# Set PYTHONPATH to include the scripts directory
export PYTHONPATH=$PYTHONPATH:$(pwd)/skills/tiktok-seller-automation/scripts

# Run the report generator
python skills/tiktok-seller-automation/scripts/generate_tiktok_report.py
```
The report will be saved to `tiktok_daily_report.json`.

## 📂 Project Structure

- `skills/tiktok-seller-automation/`: Core automation logic and Skill definition.
    - `scripts/tiktok_client.py`: The shared browser utility (Stealth, Session, Navigation).
    - `scripts/generate_tiktok_report.py`: Primary report orchestrator.
    - `scripts/auth_session.py`: Session management and login utility.
- `requirements.txt`: Python dependencies (Playwright, Playwright-Stealth, etc.).
- `.gitignore`: Configured to exclude sensitive session data and temporary reports.

## 🛠 Features
- **Stealth Integration**: Uses `playwright-stealth` and persistent browser profiles to mimic real user behavior.
- **Modular Design**: Easy to add new scrapers for different dashboard tabs (Marketing, Finance, etc.).
- **Automatic Expansion**: Automatically clicks expandable table rows to capture hidden sub-breakdowns (e.g., Affiliate vs. Linked accounts).

## 📝 License
MIT

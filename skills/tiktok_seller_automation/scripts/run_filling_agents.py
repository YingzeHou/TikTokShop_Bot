import sys
import os
import glob
# Add project root to sys.path
sys.path.append(os.getcwd())

from skills.tiktok_seller_automation.scripts.processors.product_line_processor import ProductLineProcessor

def run_filling_agents(report_file=None):
    # 1. Find the report file
    if not report_file:
        report_files = glob.glob("unified_report_*.json")
        if not report_files:
            print("No unified report found. Please run the data extraction workflow first.")
            return
        report_file = sorted(report_files)[-1]
    
    if not os.path.exists(report_file):
        print(f"Error: Report file {report_file} not found.")
        return

    print(f"Using report: {report_file}")

    # 2. Define templates and outputs
    template_dir = "templates"
    output_file = "Product_Line_Subscription_Report.xlsx"

    # Agent 1: Product Line Processor
    print("\n--- Agent: Product Line Processor ---")
    product_line_agent = ProductLineProcessor(
        template_path=os.path.join(template_dir, "Product_Line_Template.xlsx"),
        report_path=output_file
    )
    
    product_line_agent.load_raw_report(report_file)
    product_line_agent.process()

    print("\nAll specialized data-filling agents finished.")

if __name__ == "__main__":
    rep = sys.argv[1] if len(sys.argv) > 1 else None
    run_filling_agents(rep)

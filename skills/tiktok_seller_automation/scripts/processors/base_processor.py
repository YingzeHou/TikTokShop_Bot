import pandas as pd
import json
import os
from abc import ABC, abstractmethod

class BaseProcessor(ABC):
    """
    Abstract Base Class for all data-filling agents.
    Each agent must define how to load data and fill its target template.
    """
    def __init__(self, template_path, output_path):
        self.template_path = template_path
        self.output_path = output_path
        self.raw_data = None

    def load_raw_report(self, report_path):
        """Loads the unified JSON report."""
        if not os.path.exists(report_path):
            raise FileNotFoundError(f"Report not found at {report_path}")
        with open(report_path, 'r') as f:
            self.raw_data = json.load(f)
        print(f"Loaded raw report: {report_path}")

    @abstractmethod
    def process(self):
        """
        Main entry point for the agent to process raw data and fill the template.
        To be implemented by each specialized agent.
        """
        pass

    def save_result(self, df, sheet_name="Sheet2"):
        """Saves the processed DataFrame back to an Excel file."""
        df.to_excel(self.output_path, index=False, sheet_name=sheet_name)
        print(f"Successfully saved filled template to: {self.output_path}")

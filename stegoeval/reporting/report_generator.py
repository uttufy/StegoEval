import os
from stegoeval.reporting.tables import generate_csv, generate_markdown_summary
from stegoeval.reporting.plots import generate_plots
from typing import List, Dict, Any

class ReportGenerator:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self, results: List[Dict[str, Any]]):
        if not results:
            print("No results to generate reports for.")
            return

        csv_path = os.path.join(self.output_dir, "results.csv")
        md_path = os.path.join(self.output_dir, "summary.md")
        
        # Generator CSV and Markdown
        df = generate_csv(results, csv_path)
        generate_markdown_summary(df, md_path)
        
        # Generate Plots (Disabled per user request)
        # plots_dir = os.path.join(self.output_dir, "plots")
        # generate_plots(df, plots_dir)
        
        print("\n--- Benchmark Complete ---")
        print(f"Total evaluated items (Image + Attack combos): {len(results)}")
        print(f"Reports available in: {self.output_dir}")

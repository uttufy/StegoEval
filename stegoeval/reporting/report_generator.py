import os
import pandas as pd
from typing import List, Dict, Any

from stegoeval.reporting.tables import generate_csv, generate_markdown_summary
from stegoeval.scoring import calculate_overall_scores, calculate_scores_by_category


class ReportGenerator:
    def __init__(self, output_dir: str, run_name: str = "benchmark"):
        self.output_dir = output_dir
        self.run_name = run_name
        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self, results: List[Dict[str, Any]]):
        if not results:
            print("No results to generate reports for.")
            return

        # Convert to DataFrame
        df = pd.DataFrame(results)
        
        # 0. Extract and save Cover Image Baseline (if exists)
        baseline_df = df[df['algorithm'] == 'COVER_IMAGE_BASELINE']
        if not baseline_df.empty:
            baseline_csv = os.path.join(self.output_dir, f"results-{self.run_name}-baseline.csv")
            baseline_df.to_csv(baseline_csv, index=False)
            print(f"Cover image baselines saved to {baseline_csv}")
            
        # Filter out the baseline so it doesn't skew algorithm scores
        algo_df = df[df['algorithm'] != 'COVER_IMAGE_BASELINE']
        
        # 1. Save main CSV with all results
        main_csv = os.path.join(self.output_dir, f"results-{self.run_name}.csv")
        algo_df.to_csv(main_csv, index=False)
        print(f"Full algorithm results saved to {main_csv}")
        
        # 2. Generate per-attack-type CSVs
        self._generate_attack_csvs(algo_df)
        
        # 3. Generate scores file
        self._generate_scores(algo_df)
        
        # 4. Generate clean results CSV (no attack)
        clean_df = algo_df[algo_df['attack_category'] == 'none']
        if not clean_df.empty:
            clean_csv = os.path.join(self.output_dir, f"results-{self.run_name}-clean.csv")
            clean_df.to_csv(clean_csv, index=False)
            print(f"Clean results saved to {clean_csv}")
        
        # 5. Generate summary markdown
        self._generate_summary(algo_df)
        
        print("\n--- Benchmark Complete ---")
        print(f"Total evaluated items: {len(results)}")
        print(f"Reports available in: {self.output_dir}")

    def _generate_attack_csvs(self, df: pd.DataFrame):
        """Generate separate CSV files for each attack category."""
        attack_categories = df['attack_category'].unique()
        
        for category in attack_categories:
            if category == 'none':
                continue  # Already saved as clean
            
            cat_df = df[df['attack_category'] == category]
            filename = f"results-{self.run_name}-{category}.csv"
            filepath = os.path.join(self.output_dir, filename)
            cat_df.to_csv(filepath, index=False)
            print(f"{category.capitalize()} results saved to {filepath}")

    def _generate_scores(self, df: pd.DataFrame):
        """Generate scores file with StegnoEval scores."""
        # Calculate overall scores
        scores_df = calculate_overall_scores(df)
        
        if not scores_df.empty:
            scores_csv = os.path.join(self.output_dir, f"scores-{self.run_name}.csv")
            scores_df.to_csv(scores_csv, index=False)
            print(f"Scores saved to {scores_csv}")
        
        # Calculate detailed scores by category
        category_scores = calculate_scores_by_category(df)
        
        if not category_scores.empty:
            category_csv = os.path.join(self.output_dir, f"scores-{self.run_name}-by-category.csv")
            category_scores.to_csv(category_csv, index=False)
            print(f"Category scores saved to {category_csv}")

    def _generate_summary(self, df: pd.DataFrame):
        """Generate markdown summary."""
        summary_path = os.path.join(self.output_dir, f"summary-{self.run_name}.md")
        
        # Get scores
        scores_df = calculate_overall_scores(df)
        
        markdown_str = f"# StegoEval Benchmark Summary - {self.run_name}\n\n"
        
        # Overall scores table
        if not scores_df.empty:
            markdown_str += "## Overall Scores (0-100)\n\n"
            markdown_str += "| Algorithm | Compression | Blur | Noise | Geometric | Combo | Capacity | Overall |\n"
            markdown_str += "|-----------|-------------|------|-------|-----------|-------|----------|---------|\n"
            
            for _, row in scores_df.iterrows():
                comp = f"{row['compression_score']:.1f}" if row['compression_score'] else "N/A"
                blur = f"{row['blur_score']:.1f}" if row['blur_score'] else "N/A"
                noise = f"{row['noise_score']:.1f}" if pd.notna(row.get('noise_score')) and row.get('noise_score') is not None else "N/A"
                geo = f"{row['geometric_score']:.1f}" if pd.notna(row.get('geometric_score')) and row.get('geometric_score') is not None else "N/A"
                combo = f"{row['combo_score']:.1f}" if pd.notna(row.get('combo_score')) and row.get('combo_score') is not None else "N/A"
                capacity = f"{row['capacity_score']:.1f}" if pd.notna(row.get('capacity_score')) and row.get('capacity_score') is not None else "N/A"
                overall = f"{row['overall_score']:.1f}" if pd.notna(row.get('overall_score')) and row.get('overall_score') is not None else "N/A"
                
                markdown_str += f"| {row['algorithm']} | {comp} | {blur} | {noise} | {geo} | {combo} | {capacity} | {overall} |\n"
            
            markdown_str += f"\n**Recovery Rate**: {scores_df['overall_recovery_rate'].mean()*100:.1f}%\n"
        
        # Average metrics by attack
        markdown_str += "\n## Average Metrics by Attack\n\n"
        
        attack_df = df[df['attack_category'] != 'none']
        if not attack_df.empty:
            metrics = ['psnr', 'ssim', 'ber']
            available = [m for m in metrics if m in attack_df.columns]
            
            summary = attack_df.groupby('attack_category')[available].mean().reset_index()
            markdown_str += summary.to_markdown(index=False)
        
        with open(summary_path, 'w') as f:
            f.write(markdown_str)
        
        print(f"Markdown summary saved to {summary_path}")

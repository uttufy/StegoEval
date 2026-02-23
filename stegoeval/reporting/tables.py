import pandas as pd
from typing import List, Dict, Any

def generate_csv(results: List[Dict[str, Any]], filepath: str):
    """Saves the raw evaluation results to a CSV file."""
    df = pd.DataFrame(results)
    df.to_csv(filepath, index=False)
    print(f"Results saved to {filepath}")
    return df

def generate_markdown_summary(df: pd.DataFrame, filepath: str):
    """Generates a summary markdown table aggregating results by algorithm and attack."""
    
    # Group by algorithm, attack category, and attack name to get averages
    summary_cols = ['algorithm', 'attack_category', 'attack_name']
    metrics = ['psnr', 'ssim', 'ber', 'ncc_secret']
    
    # Filter columns that actually exist
    available_metrics = [m for m in metrics if m in df.columns]
    
    summary = df.groupby(summary_cols)[available_metrics].mean().reset_index()
    
    markdown_str = "# StegoEval Benchmark Summary\n\n"
    markdown_str += "## Average Performance per Algorithm & Attack\n\n"
    markdown_str += summary.to_markdown(index=False)
    
    with open(filepath, 'w') as f:
        f.write(markdown_str)
        
    print(f"Markdown summary saved to {filepath}")

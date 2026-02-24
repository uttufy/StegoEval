import typer
import yaml
import os
from typing import Optional

from stegoeval.config.schema import StegoEvalConfig
from stegoeval.core.evaluator import Evaluator
from stegoeval.reporting.report_generator import ReportGenerator

# Import algorithms
from stegoeval.stego_algorithms.example_lsb import LSBStego

app = typer.Typer(help="StegoEval: A framework for evaluating steganography algorithms.")

@app.command("info")
def info():
    """Show information about StegoEval."""
    typer.echo("StegoEval Framework v0.1.0")

@app.command("run")
def run_benchmark(
    config_path: str = typer.Option(..., "--config", "-c", help="Path to the YAML configuration file"),
    output_dir: str = typer.Option("./results", "--output", "-o", help="Directory to save evaluation results"),
    run_name: str = typer.Option("benchmark", "--name", "-n", help="Name for this benchmark run (used in output files)"),
    combo_attacks: bool = typer.Option(False, "--combo-attacks", help="Run combination attacks (all attack combinations - slower)"),
    limit: Optional[int] = typer.Option(None, "--limit", "-l", help="Limit number of images to test")
):
    """
    Run the benchmarking workflow using the provided configuration.
    """
    typer.echo(f"Starting StegoEval with config: {config_path}")
    
    # Load configuration
    try:
        with open(config_path, "r") as f:
            raw_config = yaml.safe_load(f)
        
        # Override config with CLI arguments
        if run_name:
            raw_config['run_name'] = run_name
        if combo_attacks:
            raw_config['combo_attacks'] = combo_attacks
        if limit is not None:
            raw_config['dataset_limit'] = limit
        
        # Validate config
        config = StegoEvalConfig(**raw_config).model_dump()
        
    except Exception as e:
        typer.echo(f"Error loading configuration: {e}", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Dataset path: {config['dataset_path']}")
    limit_str = str(config['dataset_limit']) if config['dataset_limit'] else 'All'
    typer.echo(f"Dataset limit: {limit_str}")
    typer.echo(f"Output directory: {output_dir}")
    typer.echo(f"Run name: {config['run_name']}")
    typer.echo(f"Combo attacks: {config['combo_attacks']}")

    # Register algorithms to evaluate
    algorithms = [
        LSBStego()
        # Add more algorithms here
    ]
    
    algo_names = [a.name() for a in algorithms]
    typer.echo(f"Loaded algorithms: {', '.join(algo_names)}")

    # Initialize Evaluator
    evaluator = Evaluator(config=config, algorithms=algorithms)
    
    # Run evaluation
    results = evaluator.evaluate()
    
    # Generate Reports (capacity is now included in evaluator if enabled)
    reporter = ReportGenerator(output_dir=output_dir, run_name=config['run_name'])
    reporter.generate(results)

    typer.echo(f"\n--- Benchmark Complete ---")
    typer.echo(f"Results saved to: {output_dir}")

if __name__ == "__main__":
    app()

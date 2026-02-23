import os
import __main__

# This file would typically show how a user could programmatically call StegoEval
# But we can also just provide a simple runner that invokes the CLI.

print("To run the benchmark programmatically, see stegoeval/cli.py -> function 'run()'")
print("Or simply execute in the terminal:")
print("stegoeval run --config config/default_config.yaml")

# Example programmatic usage
from stegoeval.config.schema import StegoEvalConfig
from stegoeval.core.evaluator import Evaluator
from stegoeval.reporting.report_generator import ReportGenerator
from stegoeval.stego_algorithms.example_lsb import LSBStego
import yaml

def run_example_programmatically():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "default_config.yaml")
    
    with open(config_path, "r") as f:
        config_data = yaml.safe_load(f)
        
    config = StegoEvalConfig(**config_data).model_dump()
    
    evaluator = Evaluator(config=config, algorithms=[LSBStego()])
    results = evaluator.evaluate()
    
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results_programmatic")
    reporter = ReportGenerator(output_dir=output_dir)
    reporter.generate(results)
    print(f"Programmatic evaluation complete. Results in {output_dir}")

if __name__ == "__main__":
    reply = input("Run programmatic example now? (y/n): ")
    if reply.lower() == 'y':
        run_example_programmatically()

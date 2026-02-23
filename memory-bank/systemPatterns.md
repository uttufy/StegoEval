# StegoEval — System Patterns

## Architecture Overview

```
stegoeval/
├── cli.py                    # Typer CLI entry point (commands: run, info)
├── config/
│   └── schema.py             # Pydantic config model (StegoEvalConfig)
├── core/
│   ├── evaluator.py          # Main orchestrator (Evaluator class)
│   ├── attack_runner.py      # Attack dispatch engine (AttackRunner class)
│   └── dataset_loader.py     # Recursive image scanner (DatasetLoader class)
├── attacks/
│   ├── compression.py        # JPEG, WebP compression attacks
│   ├── noise.py              # Gaussian, Salt & Pepper, Speckle, Poisson noise
│   ├── filtering.py          # Gaussian Blur, Median Filter, Motion Blur
│   └── geometric.py          # Rotation, Scaling, Cropping, Resize
├── metrics/
│   ├── distortion.py         # MSE, RMSE, PSNR, SSIM, AAD, NAD, NCC (image)
│   └── robustness.py         # BER, NCC (text), NPCR, UACI (image payloads)
├── reporting/
│   ├── report_generator.py   # Orchestrates CSV, Markdown, and Plot generation
│   ├── tables.py             # CSV export + Markdown summary aggregation
│   └── plots.py              # Matplotlib/Seaborn charts (currently disabled)
└── stego_algorithms/
    ├── base.py               # StegoAlgorithm ABC (embed, extract, name)
    ├── example_lsb.py        # Built-in LSB reference implementation
    └── example_cli_adapter.py # GenericCLIAdapter for external CLI tools
```

## Key Design Patterns

### 1. Strategy Pattern — Algorithm Pluggability
- `StegoAlgorithm` is an abstract base class with 3 methods: `embed(cover, payload) → stego`, `extract(stego) → payload`, `name() → str`
- Algorithms are instantiated and passed as a list to `Evaluator`
- Adding a new algorithm = one new class + one import in `cli.py`

### 2. Registry Pattern — Attack Dispatch
- `AttackRunner` maintains a nested dict mapping `category → attack_name → function`
- Uses `inspect.signature()` to dynamically infer parameter names for single-value configs
- Supports both dict-style params (`{mean: 0.0, var: 0.01}`) and scalar params (`95`)

### 3. Adapter Pattern — External CLI Integration
- `GenericCLIAdapter` bridges file-based CLI tools into StegoEval's in-memory ndarray workflow
- Saves ndarray → temp file → runs subprocess → reads result back to ndarray
- Supports external venvs via custom `python_exec` path

### 4. Configuration-Driven Execution
- YAML config defines dataset path, payload, and complete attack matrix
- Validated at load time via Pydantic `StegoEvalConfig`
- Config is passed as a plain dict through the system after validation

## Data Flow

```
YAML Config → Pydantic Validation → Evaluator
                                       │
                                       ├── DatasetLoader (scans images)
                                       │
                                       ├── For each (image × algorithm × payload_size):
                                       │     ├── algorithm.embed(cover, payload)
                                       │     ├── Compute distortion metrics (cover vs stego)
                                       │     ├── algorithm.extract(stego) → clean BER check
                                       │     │
                                       │     └── For each attack config:
                                       │           ├── AttackRunner.run_attacks(stego, config)
                                       │           ├── algorithm.extract(attacked_stego)
                                       │           └── Compute robustness metrics
                                       │
                                       └── ReportGenerator
                                             ├── CSV (raw results)
                                             ├── Markdown summary (grouped averages)
                                             └── Plots (optional, currently disabled)
```

## Component Relationships

| Component | Depends On | Provides |
|-----------|-----------|----------|
| `cli.py` | config/schema, core/evaluator, reporting, stego_algorithms | CLI entry points |
| `Evaluator` | DatasetLoader, AttackRunner, StegoAlgorithm, metrics | Benchmark results list |
| `AttackRunner` | attacks/* modules | Generator of attacked images |
| `DatasetLoader` | OpenCV | Generator of (filename, ndarray) tuples |
| `ReportGenerator` | tables, plots | CSV, Markdown, PNG files |
| `StegoAlgorithm` | numpy | Abstract interface for all algorithms |

## Critical Implementation Details

- **Dimension Mismatch Handling**: `_match_dims()` in `distortion.py` resizes stego to match cover dimensions before metric computation (needed for geometric attacks that change image size).
- **Error Recovery**: If `embed()` fails (e.g., payload too large), the evaluator logs the error, skips remaining payload sizes for that image/algo combo, and continues.
- **Payload Generation**: Random payloads of configurable sizes are generated per run (not taken from config's `payload` field — that field appears unused by the evaluator).
- **Plot Generation**: Currently disabled in `ReportGenerator` (commented out).

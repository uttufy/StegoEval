# StegoEval — Active Context

## Current Work Focus

- Memory bank initialization for the StegoEval project.
- The project is in a **stable MVP state** — the core benchmarking pipeline works end-to-end with the built-in LSB algorithm.

## Recent Changes

- Fixed Python version incompatibility in GitHub Actions workflow (was using 3.10, now correctly set to 3.11).
- Added Zensical-based documentation with auto-deploy to GitHub Pages.
- Project has been used to produce a `results.csv` with ~2.1MB of benchmark data.

## Active Decisions

- **Plot generation is disabled** in `ReportGenerator` — the `generate_plots()` call is commented out. Likely a deliberate choice to speed up benchmarks or because plots needed refinement.
- **Payload sizes are hardcoded** in the evaluator defaults (`[10, 100, 1000, 5000, 10000]`), not driven by YAML config. The config's `payload` field is currently unused by the evaluator.
- **Only one algorithm is registered** — `LSBStego`. The framework supports multiple but none are added yet.

## Important Patterns & Preferences

- Algorithms are registered manually in `cli.py` by import + list append.
- External CLI tools use the `GenericCLIAdapter` pattern with subprocess isolation.
- All image data is `numpy.ndarray` throughout the pipeline.
- Config is YAML → Pydantic → plain dict (uses `model_dump()`).

## Next Steps

- Add more steganography algorithms for comparative evaluation.
- Re-enable and polish plot generation.
- Wire up the `payload` and `payload_sizes` config fields to Evaluator.
- Add unit tests (the `tests/` directory exists but is empty).
- Consider adding a survivability score metric as mentioned in related StegoBench design conversations.

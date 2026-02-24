# StegoEval — Active Context

## Current Work Focus

- Completed major restructuring of the StegoEval benchmark framework.
- The project is in **v0.2.0 state** — enhanced benchmarking with real-world attack levels and scoring.

## Recent Changes (v0.2.0)

1. **Added Real-World Attack Levels**:
   - Compression: JPEG/WebP at 10%, 20%, 50%, 60%, 80%, 90%
   - Blur: Gaussian kernels 3, 5, 7, 9, 11
   - Cropping: 1%, 5%, 10%, 20%, 30%, 50%
   - Rotation: ±2°, ±5°, ±10°, ±15°, ±30°
   - Scaling: 0.5x, 0.8x, 1.2x, 1.5x, 2.0x

2. **Added StegnoEval Score**:
   - Composite score 0-100
   - Formula: (Distortion × 0.4) + (Robustness × 0.6)
   - Separate scores per attack category

3. **Added Per-Attack CSV Outputs**:
   - `results-{run_name}.csv` (main)
   - `results-{run_name}-clean.csv`
   - `results-{run_name}-compression.csv`
   - `results-{run_name}-filtering.csv`
   - `results-{run_name}-noise.csv`
   - `results-{run_name}-geometric.csv`
   - `results-{run_name}-combo.csv`

4. **Added Scoring Files**:
   - `scores-{run_name}.csv` (overall scores)
   - `scores-{run_name}-by-category.csv` (detailed breakdown)

5. **Added Combination Attacks**:
   - Flag: `--combo-attacks`
   - Runs all attack combinations when enabled

6. **Added Run Names**:
   - Flag: `--name` or `-n`
   - Output files use run name prefix

7. **Removed Plots**:
   - Plot generation explicitly disabled for speed
   - Can be re-enabled by editing `plots.py`

## Active Decisions

- **Image filename as primary key** — All CSV files use `image` column as primary key for joins/relationships.
- **Random payloads** — Still using random payloads per test (config's `payload` field not yet wired).
- **Only LSB algorithm** — Framework supports multiple but only one built-in.

## Important Patterns & Preferences

- Algorithms are registered manually in `cli.py` by import + list append.
- External CLI tools use the `GenericCLIAdapter` pattern with subprocess isolation.
- All image data is `numpy.ndarray` throughout the pipeline.
- Config is YAML → Pydantic → plain dict (uses `model_dump()`).
- Results organized by attack category for easier analysis.
- **Capacity as attack category** - Capacity test now runs as part of benchmark (like compression/noise) when `capacity.enabled: true` in config.

## Recent Changes (v0.2.1)

8. **Added Capacity Test Integration**:
   - Capacity now runs as part of `stegoeval run` when enabled in config
   - Config: `capacity.enabled: true`, `capacity.max_payload`, `capacity.step`
   - Results in main CSV with `attack_category: "capacity"`
   - Separate capacity CSV also generated: `results-{run_name}-capacity.csv`

## Next Steps

- Add more steganography algorithms for comparative evaluation.
- Wire up the `payload` config field to Evaluator.
- Add unit tests (the `tests/` directory exists but is empty).
- Consider adding a survivability score metric as mentioned in related StegoBench design conversations.

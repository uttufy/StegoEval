# StegoEval — Progress

## What Works ✅

- **CLI** — `stegoeval run` and `stegoeval info` commands functional via Typer.
- **Config System** — YAML loading + Pydantic validation with `StegoEvalConfig`.
- **Dataset Loader** — Recursive image scanning with multi-format support (PNG, JPG, BMP, TIFF).
- **Dataset Download Script** — Downloads 100 grayscale + 100 color Picsum images + 5 synthetic.
- **Evaluator Loop** — Full benchmark over images × algorithms × payload_sizes with error recovery.
- **Attack Engine** — 12 attack functions across 4 categories (compression, noise, filtering, geometric) with registry-based dispatch.
- **Distortion Metrics** — MSE, RMSE, PSNR, SSIM, AAD, NAD, NCC with dimension mismatch handling.
- **Robustness Metrics** — BER and NCC for text payloads; NPCR and UACI available for image payloads.
- **Reporting** — CSV export and grouped Markdown summary table generation.
- **LSB Algorithm** — Built-in reference implementation with binary embedding/extraction.
- **CLI Adapter** — `GenericCLIAdapter` template for integrating external CLI tools (subprocess-based).
- **Documentation** — Zensical-powered docs auto-deployed to GitHub Pages.
- **Setup Script** — `setup.sh` for one-command environment setup.

## What's Left to Build 🔲

- [ ] Unit / integration tests (empty `tests/` directory).
- [ ] Additional steganography algorithms beyond LSB (e.g., DCT-based, DWT-based, IWT-SVD).
- [ ] Re-enable and polish plot generation (currently commented out).
- [ ] Wire `payload` and `payload_sizes` from YAML config into Evaluator.
- [ ] Add composite survivability score metric.
- [ ] Add steganalysis detection metrics (optional expansion).
- [ ] Set up CI for tests (only docs CI exists).
- [ ] Publish to PyPI.
- [ ] Fill out docs content (currently skeleton `index.md` and `contributing.md`).

## Known Issues ⚠️

1. **Config `payload` field unused** — Evaluator generates random payloads instead of using the config's `payload` value.
2. **`payload_sizes` not configurable** — Hardcoded default in evaluator, not sourced from YAML config.
3. **Plots disabled** — `generate_plots()` call is commented out in `ReportGenerator.generate()`.
4. **No test coverage** — `tests/` directory is empty.
5. **Dimension mismatch after geometric attacks** — Handled via resize in metrics, but may introduce comparison artifacts.

## Project Evolution

- **v0.1.0 (Current)** — MVP with full pipeline: config → load → embed → metrics → attacks → report. Single built-in algorithm (LSB). YAML-driven attack matrix. CSV + Markdown output.
- **Related Project: StegoBench** — A more ambitious benchmarking framework design was explored in recent conversations, potentially informing future StegoEval features (survivability scoring, more sophisticated reporting).
- **Related Project: DeepSign** — A broader steganography platform ecosystem (engine, worker, API, frontend) that this tool could integrate with for algorithm evaluation.

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
- **Reporting** — CSV export (per attack type), Markdown summary, and StegnoEval scores.
- **LSB Algorithm** — Built-in reference implementation with binary embedding/extraction.
- **CLI Adapter** — `GenericCLIAdapter` template for integrating external CLI tools (subprocess-based).
- **Documentation** — Zensical-powered docs auto-deployed to GitHub Pages + CSV structure docs.
- **Setup Script** — `setup.sh` for one-command environment setup.
- **StegnoEval Score** — Composite scoring system (0-100) based on distortion + robustness.
- **Combo Attacks** — Flag to run all attack combinations.
- **Run Names** — Custom benchmark run names for output files.
- **Real-world Attack Levels** — Comprehensive attack levels (JPEG 10-90%, blur kernels 3-11, etc.)

## What's Left to Build 🔲

- [ ] Unit / integration tests (empty `tests/` directory).
- [ ] Additional steganography algorithms beyond LSB (e.g., DCT-based, DWT-based, IWT-SVD).
- [ ] Re-enable and polish plot generation (currently disabled).
- [ ] Add steganalysis detection metrics (optional expansion).
- [ ] Set up CI for tests (only docs CI exists).
- [ ] Publish to PyPI.
- [ ] Fill out docs content (currently skeleton `index.md` and `contributing.md`).

## Known Issues ⚠️

1. **Config `payload` field unused** — Evaluator generates random payloads instead of using the config's `payload` value.
2. **`payload_sizes` now configurable** — ✅ Fixed (added to config).
3. **Plots disabled** — ✅ Fixed (explicitly disabled, can be re-enabled).
4. **No test coverage** — `tests/` directory is empty.
5. **Dimension mismatch after geometric attacks** — Handled via resize in metrics, but may introduce comparison artifacts.

## Project Evolution

- **v0.1.0 (MVP)** — Initial release with core pipeline.
- **v0.2.0 (Current)** — Major update with:
  - Real-world attack levels (JPEG 10-90%, blur 3-11, crop 1-50%, rotation ±2-30°, scale 0.5-2x)
  - StegnoEval Score (0-100 composite score)
  - Per-attack CSV outputs
  - Combination attack support (flag: `--combo-attacks`)
  - Custom run names (`--name`)
  - Image filename as primary key for all CSVs
  - Comprehensive CSV structure documentation

# StegoEval — Product Context

## Why This Project Exists

Steganography research papers often evaluate algorithms using ad-hoc, one-off scripts with inconsistent metrics and attack configurations. This makes **fair comparison** between techniques difficult and results hard to reproduce. StegoEval solves this by providing a **standardized evaluation pipeline** that any algorithm can plug into.

## Problems It Solves

1. **Inconsistent Benchmarking** — Different papers use different metrics, datasets, and attack types. StegoEval enforces a uniform evaluation protocol.
2. **Tedious Setup** — Researchers spend time building evaluation harnesses instead of focusing on algorithms. StegoEval provides this out of the box.
3. **External Tool Integration** — Many steganography tools are CLI-based with their own virtual environments. The `GenericCLIAdapter` bridges this gap seamlessly.
4. **Reproducibility** — YAML-driven configuration ensures benchmarks can be exactly replicated.

## How It Works (User Journey)

1. **Install** — `pip install -e .` (or clone + setup.sh)
2. **Prepare Data** — `python scripts/download_datasets.py` downloads Picsum images + generates synthetic test images into `./data/`
3. **Configure** — Edit `config/default_config.yaml` to set dataset path, payload text, attack parameters
4. **Run** — `stegoeval run --config config/default_config.yaml --output ./results`
5. **Review** — Examine `results/results.csv` (raw data), `results/summary.md` (aggregated Markdown table), and optionally `results/plots/` (visual charts)

## User Experience Goals

- **Zero-friction algorithm integration** — Implement 3 methods (`embed`, `extract`, `name`) and you're done.
- **One command benchmarking** — A single CLI command runs hundreds of configurations.
- **Human-readable outputs** — Results are in CSV + Markdown, immediately usable in papers.
- **Fail-safe evaluation** — If a payload is too large or an attack crashes, the framework logs the error and continues.

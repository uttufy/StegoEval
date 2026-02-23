# StegoEval

A modular benchmarking framework to evaluate steganography algorithms under real-world conditions.

## Features

- Compare Cover vs Stego image distortion.
- Test robustness under real-world attacks (compression, noise, filtering, geometric).
- Measure secret extraction accuracy.
- Produce tabular & graphical evaluation reports.
- Easily plug in multiple steganography algorithms.
- Supports RGB, Grayscale, and synthetic graphics images.

## Installation

```bash
git clone https://github.com/yourusername/StegoEval.git
cd StegoEval
pip install -e .
```

## Prepare Test Data

Download subsets of BOSSBase, DIV2K, and generate synthetic images:

```bash
python scripts/download_datasets.py
```

## Usage

Run a benchmark using a YAML configuration file:

```bash
stegoeval run --config config/default_config.yaml
```

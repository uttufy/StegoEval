<p align="center">
  <img src="docs/assets/logos/flare.png" alt="StegoEval Logo" width="200" />
</p>

# StegoEval

[![Docs](https://github.com/uttufy/StegoEval/actions/workflows/docs.yml/badge.svg)](https://uttufy.github.io/StegoEval/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)

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
git clone https://github.com/uttufy/StegoEval.git
cd StegoEval
pip install -e .
```

## Prepare Test Data

Download subsets of BOSSBase, DIV2K, and generate synthetic images:

```bash
python scripts/download_datasets.py
```

## Usage

### Run Full Benchmark

Run a benchmark using a YAML configuration file:

```bash
stegoeval run --config config/default_config.yaml
```

Capacity test is automatically run as part of the benchmark when enabled in config:

```yaml
capacity:
  enabled: true
  max_payload: 10000
  step: 100
```

### Run Capacity Test Only

Test the embedding capacity of algorithms separately:

```bash
stegoeval capacity --config config/default_config.yaml --max-payload 10000 --step 100
```

Options:
- `--max-payload, -m`: Maximum payload size to test (default: 10000)
- `--step, -s`: Step size for payload increments (default: 100)
- `--limit, -l`: Limit number of images to test

## Metrics Dictionary

When running `stegoeval run`, a `results.csv` file is generated. Here is what each column means:

### General Information
- **`image`**: The filename of the cover image tested.
- **`algorithm`**: The name of the Steganography algorithm used.
- **`payload_size`**: The number of characters embedded as the secret payload. Used to test the maximum capacity.
- **`attack_category`**: The type of attack applied to the stego image (e.g., `compression`, `noise`, `geometric`, or `none`).
- **`attack_name`**: The specific attack applied (e.g., `jpeg`, `gaussian`, `rotate`, or `clean`).
- **`attack_params`**: The parameters of the attack (e.g., quality factor, noise variance, rotation angle).

### Distortion Metrics (Cover Image vs. Clean Stego Image)
These metrics determine how much visual degradation occurred just by embedding the secret.
- **`mse` (Mean Squared Error)**: Measures average squared difference between Cover and Stego pixels. Lower is better (0 = identical).
- **`rmse` (Root MSE)**: The square root of MSE, putting it back in the pixel value domain (0-255). Lower is better.
- **`psnr` (Peak Signal-to-Noise Ratio)**: Expressed in decibels (dB). Higher is better. Usually, >30dB is considered acceptable, and >40dB means the distortion is virtually imperceptible to the human eye.
- **`ssim` (Structural Similarity Index Measure)**: Measures the perceived change in structural information. Ranges from 0 to 1, where 1 means identical. Higher is better.
- **`aad` (Average Absolute Difference)**: The average absolute pixel-by-pixel difference. Lower is better.
- **`nad` (Normalized Absolute Difference)**: The absolute difference normalized by the cover image's total pixel summation. Lower is better.
- **`ncc_image` (Normalized Cross-Correlation)**: Measures similarity between the two images. Closer to 1.0 means highly correlated/identical.

### Robustness Metrics (Clean Stego Image vs. Attacked Stego Image)
These metrics determine if the payload can survive image degradation.
- **`psnr_attacked`**: The PSNR between the original Cover image and the Attacked Stego Image. Shows how badly the attack ruined the visual quality.
- **`ssim_attacked`**: The SSIM between the original Cover image and the Attacked Stego Image.
- **`embedded_payload`**: The original text string that was embedded into the cover image.
- **`extracted_payload`**: The text string that was extracted from the stego image (either clean or post-attack).
- **`ber` (Bit Error Rate)**: The percentage of characters/bits that were corrupted upon extraction. Ranges from 0.0 to 1.0. **Lower is better (0.0 = perfect extraction).**
- **`ncc_secret`**: The Normalized Cross-Correlation between the original payload string and the extracted payload string based on ASCII values. **Higher is better (1.0 = perfect match).**

## Evaluating External CLI Tools (Wrappers)

A common use case in research is to evaluate code from an existing paper built as a python CLI that demands specific file paths (like saving a `.npy` key file to disk during embedding, and passing it along during extraction) or operates inside its own isolated Python virtual environment.

To use an external CLI tool seamlessly within **StegoEval's** in-memory workflow, you simply use an adapter script! We have provided a fully generic wrapper in `stegoeval/stego_algorithms/example_cli_adapter.py`.

### How to use:
1. Copy `example_cli_adapter.py` and modify the internal wrapper `embed` and `extract` methods to match the exact `subprocess` command syntax of your target CLI script.
2. If the external project uses its own virtual environment with conflicting dependencies (like older TensorFlow versions), you can tell the adapter to use the specific `python` executable inside that `.venv`!
3. Import your adapter inside `stegoeval/cli.py` and append it to the `algorithms` array:

```python
# stegoeval/cli.py
from stegoeval.stego_algorithms.example_cli_adapter import GenericCLIAdapter

algorithms = [
    LSBStego(),
    GenericCLIAdapter(
        cli_script_path="/path/to/their/script.py",
        venv_python_path="/path/to/their/.venv/bin/python" # Executes using their environment!
    )
]
```
Running `stegoeval run` will now execute your 500+ benchmark configurations against their CLI reliably without crashing your StegoEval environment.

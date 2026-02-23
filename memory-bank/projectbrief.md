# StegoEval — Project Brief

## Overview

**StegoEval** is a modular, research-grade benchmarking framework for evaluating steganography algorithms under real-world conditions. It is a Python package (v0.1.0) distributed as an installable CLI tool.

**Repository**: [github.com/uttufy/StegoEval](https://github.com/uttufy/StegoEval)
**Documentation**: [uttufy.github.io/StegoEval](https://uttufy.github.io/StegoEval/)

## Core Requirements

1. **Distortion Evaluation** — Compare Cover vs. Stego image quality using MSE, RMSE, PSNR, SSIM, AAD, NAD, and NCC metrics.
2. **Robustness Testing** — Subject stego images to real-world attacks (compression, noise, filtering, geometric) and measure payload survivability via BER and NCC.
3. **Capacity Testing** — Evaluate algorithms across increasing payload sizes (10 → 10,000+ chars) to find capacity limits.
4. **Comprehensive Reporting** — Generate CSV data files, Markdown summary tables, and matplotlib/seaborn plots.
5. **Extensibility** — Support plugging in new steganography algorithms via a simple abstract base class or CLI adapter pattern.
6. **Dataset Flexibility** — Support RGB, grayscale, and synthetic images across multiple dataset sources (Picsum, BOSSBase, DIV2K, custom).

## Goals

- Provide a standardized, reproducible benchmarking pipeline for steganography research.
- Enable fair, side-by-side comparison of multiple steganography algorithms.
- Make it trivial to add new algorithms, attacks, and metrics.
- Produce publication-ready evaluation tables and figures.

## Non-Goals

- StegoEval is **not** a steganography library — it benchmarks algorithms, not implements them.
- It does not provide steganalysis / detection capabilities.
- Real-time or streaming steganography is out of scope.

## Target Users

- Academic researchers evaluating novel steganography techniques.
- Security professionals assessing steganographic robustness.
- Students learning about image steganography through hands-on experimentation.

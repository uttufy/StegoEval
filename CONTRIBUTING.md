# Contributing to StegoEval

First off, thank you for considering contributing to StegoEval! It's people like you that make StegoEval a great framework for benchmarking steganography algorithms.

## Where to Start

- **Bug Reports**: If you find a bug, please open an issue and include as much detail as possible (logs, configurations, etc.).
- **Feature Requests**: Have an idea for a new attack, metric, or feature? Open an issue and let's discuss it!
- **Code Contributions**: Pull requests are very welcome!

## Development Setup

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/uttufy/StegoEval.git
   cd StegoEval
   ```
3. **Set up a virtual environment** and install the project in writable mode along with development dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   pip install zensical
   ```

## Adding a New Algorithm

All steganography algorithms must inherit from the `StegoAlgorithm` base class found in `stegoeval/stego_algorithms/base.py`.

1. Create a new python file in `stegoeval/stego_algorithms/`.
2. Inherit from `StegoAlgorithm` and implement `embed()`, `extract()`, and `name()`.
3. If it's a wrapper for an external CLI, use the Generic CLI Adapter pattern.
4. Add your algorithm to the `algorithms` array in `stegoeval/cli.py` or provide instructions on how users can inject it.

## Adding a New Attack

1. Find the appropriate category in `stegoeval/attacks/` (e.g., `noise.py`, `filtering.py`) or create a new one.
2. Implement your attack function. The function should take a `numpy.ndarray` image as the first argument, and return the modified image as a `numpy.ndarray`.
3. Register your attack inside the `AttackRunner` class in `stegoeval/core/attack_runner.py`.

## Building the Documentation

We use [Zensical](https://zensical.org/) to auto-generate documentation from our Python docstrings.

To view the documentation locally:
```bash
zensical serve
```
Then open `http://127.0.0.1:8000` in your browser.

## Submitting a Pull Request

1. Create a new branch for your feature (`git checkout -b feature/amazing-feature`).
2. Make your necessary changes.
3. Update the documentation to reflect your changes.
4. Commit your changes (`git commit -m 'Add amazing feature'`).
5. Push to the branch (`git push origin feature/amazing-feature`).
6. Open a Pull Request on GitHub.

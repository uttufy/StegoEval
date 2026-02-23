# StegoEval — Tech Context

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python ≥ 3.11 | Core language |
| CLI | Typer | CLI framework with help generation |
| Config Validation | Pydantic | YAML config → validated model |
| Image Processing | OpenCV (headless), Pillow | Image I/O, attacks, transforms |
| Scientific Computing | NumPy, SciPy, scikit-image | Metrics, array operations |
| Data Analysis | Pandas | Result aggregation, CSV export |
| Visualization | Matplotlib, Seaborn | Chart generation |
| Reporting | tabulate | Markdown table formatting |
| HTTP | Requests | Dataset downloading |
| Config Format | PyYAML | YAML parsing |
| Documentation | Zensical + mkdocstrings | Auto-generated docs from docstrings |
| Build System | setuptools (≥ 61.0) | Package building |

## Development Setup

```bash
# Clone and setup
git clone https://github.com/uttufy/StegoEval.git
cd StegoEval
bash setup.sh          # Creates .venv, installs deps, installs package in editable mode

# Or manually:
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# Download test data
python scripts/download_datasets.py
```

## Project Entry Point

```toml
# pyproject.toml
[project.scripts]
stegoeval = "stegoeval.cli:app"     # CLI via typer
```

## Key Dependencies

### Runtime
- `numpy`, `opencv-python-headless`, `scikit-image`, `scipy` — Image processing and metrics
- `matplotlib`, `pandas`, `seaborn`, `tabulate` — Reporting
- `typer`, `pydantic`, `pyyaml` — CLI and config
- `requests`, `Pillow` — Data downloading and synthetic image generation
- `tqdm` — Progress bars
- `zensical` — Documentation generation tool

### Dev/Docs
- `mkdocstrings[python]` — Auto API docs from docstrings
- `pymdown-extensions` — Enhanced Markdown rendering in docs

## CI/CD

- **GitHub Actions**: `.github/workflows/docs.yml`
  - Triggers on push to `master` or manual dispatch
  - Python 3.11, installs deps, runs `zensical build`, deploys to GitHub Pages
  - No test CI configured yet

## Data Directory Structure

```
data/
├── picsum_color/     # 100 color images from Picsum (512×512 JPG)
├── picsum_gray/      # 100 grayscale images from Picsum (512×512 JPG)
└── synthetic/        # 5 generated images (random RGB + geometric patterns, 512×512 PNG)
```

## Output Directory Structure

```
results/
├── results.csv       # Raw evaluation data (all metrics × all configs)
├── summary.md        # Aggregated Markdown table
└── plots/            # (Optional) Generated chart PNGs
```

## Technical Constraints

- Requires Python ≥ 3.11 (uses modern typing features)
- Images loaded via `cv2.imread(IMREAD_UNCHANGED)` — preserves original channels
- All image data flows as `numpy.ndarray` (uint8, shape HxW or HxWxC)
- Attack functions must accept `np.ndarray` as first arg and return `np.ndarray`
- CLI adapter uses `subprocess` — external tools run in isolation

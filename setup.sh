#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "======================================"
echo "    StegoEval Environment Setup        "
echo "======================================"

# 1. Create the virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment in .venv..."
    python3 -m venv .venv
else
    echo "Virtual environment .venv already exists."
fi

# 2. Activate the virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# 3. Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# 4. Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing requirements from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found!"
    exit 1
fi

# 5. Install the package in editable mode
echo "Installing StegoEval package in editable mode..."
pip install -e .

echo "======================================"
echo "Setup complete! To activate the environment, run:"
echo "source .venv/bin/activate"
echo "======================================"

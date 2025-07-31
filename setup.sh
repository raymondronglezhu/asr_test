#!/bin/bash

echo "Setting up Skywalk vs Nothing ENC Test Environment"
echo "=================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Create data directories if they don't exist
echo "Creating data directories..."
mkdir -p data/skywalk
mkdir -p data/nothing

echo ""
echo "Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Place your audio files in data/skywalk/ and data/nothing/"
echo "2. Ensure files follow the naming convention (e.g., ACB.wav)"
echo "3. Run: python test_script.py"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "source venv/bin/activate" 
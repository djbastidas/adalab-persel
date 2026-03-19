#!/bin/bash
# Setup script for Ecuador Real Estate Rental Price Prediction

echo "================================"
echo "Setting up project environment"
echo "================================"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p data
mkdir -p models
mkdir -p api

# Run EDA
echo ""
echo "================================"
echo "Running EDA and Data Cleaning..."
echo "================================"
python 1_eda_complete.py

# Run Modeling
echo ""
echo "================================"
echo "Building and Training Model..."
echo "================================"
python 2_modeling_complete.py

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "To start the API server, run:"
echo "  source venv/bin/activate"
echo "  python -m api.app"
echo ""
echo "Or use Gunicorn for production:"
echo "  gunicorn -w 4 -b 0.0.0.0:5000 api.app:app"
echo ""

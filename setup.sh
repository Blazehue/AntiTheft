#!/bin/bash
# Anti-Theft Alarm System - Setup Script for Linux/Mac

echo "==============================================="
echo "Anti-Theft Alarm System - Setup Script"
echo "==============================================="
echo ""

# Check Python installation
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found! Please install Python 3.8 or higher."
    exit 1
fi
python3 --version
echo ""

# Create virtual environment
echo "[2/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi
echo ""

# Activate virtual environment
echo "[3/5] Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "[4/5] Installing dependencies..."
echo "This may take several minutes..."
pip install --upgrade pip
pip install -r requirements.txt
echo ""

# Create storage directories
echo "[5/5] Creating storage directories..."
mkdir -p storage/intruders
mkdir -p storage/logs
mkdir -p storage/authorized_faces
echo "Storage directories created."
echo ""

echo "==============================================="
echo "Setup Complete!"
echo "==============================================="
echo ""
echo "To run the system:"
echo "  1. Activate venv: source venv/bin/activate"
echo "  2. Run: python main.py"
echo ""
echo "Optional: Add authorized face images to:"
echo "  storage/authorized_faces/person_name.jpg"
echo ""

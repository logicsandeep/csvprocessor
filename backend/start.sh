#!/bin/bash

# CSV Processor Startup Script for Linux/macOS

echo "🚀 Starting CSV Processor..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    echo "Visit: https://www.python.org/downloads/"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Check if installation was successful
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Please check your Python setup."
    exit 1
fi

# Start the server
echo "🌐 Starting server on http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""

python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

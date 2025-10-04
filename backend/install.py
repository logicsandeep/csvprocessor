#!/usr/bin/env python3
"""
CSV Processor Installation Script
This script helps set up the CSV Processor on any system.
"""

import sys
import subprocess
import os
import platform

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_startup_script():
    """Create a platform-specific startup script"""
    system = platform.system().lower()
    
    if system == "windows":
        script_content = """@echo off
echo Starting CSV Processor...
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
"""
        with open("run.bat", "w") as f:
            f.write(script_content)
        print("✅ Created run.bat for Windows")
        
    else:  # Linux/macOS
        script_content = """#!/bin/bash
echo Starting CSV Processor...
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""
        with open("run.sh", "w") as f:
            f.write(script_content)
        os.chmod("run.sh", 0o755)
        print("✅ Created run.sh for Unix systems")

def main():
    """Main installation function"""
    print("🚀 CSV Processor Installation")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create startup script
    create_startup_script()
    
    print("\n🎉 Installation completed successfully!")
    print("\nTo start the application:")
    
    system = platform.system().lower()
    if system == "windows":
        print("  Windows: Double-click run.bat or run 'python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000'")
    else:
        print("  Linux/macOS: Run './run.sh' or 'python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000'")
    
    print("\nThen open your browser and go to: http://localhost:8000")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)

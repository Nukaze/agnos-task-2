#!/usr/bin/env python3
"""
Symptom Recommendation System Server Runner

This script starts the FastAPI server with proper configuration and error handling.
"""

import uvicorn
import sys
import os
from pathlib import Path
import subprocess

def check_dependencies():
    """Check if all required dependencies are available"""
    try:
        import fastapi
        import pandas
        import numpy
        import sklearn
        import joblib
        print("✓ All dependencies are available")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def check_data_file():
    """Check if the data file exists"""
    data_file = Path("ai_symptom_picker.csv")
    if data_file.exists():
        print(f"✓ Data file found: {data_file}")
        return True
    else:
        print(f"✗ Data file not found: {data_file}")
        print("Please ensure ai_symptom_picker.csv is in the current directory")
        return False

def main():
    
    """Main function to run the server"""
    print("=" * 60)
    print("Symptom Recommendation System API")
    print("=" * 60)
    
    # Check prerequisites
    print("\nChecking prerequisites...")
    if not check_dependencies():
        sys.exit(1)
    
    if not check_data_file():
        sys.exit(1)
    
    # Server configuration
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 8000))
    
    print(f"\nStarting server...")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"API Documentation: http://{host}:{port}/docs")
    print(f"Health Check: http://{host}:{port}/")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Start the server
        uvicorn.run(
            "app:app",
            host=host,
            port=port,
            reload=True,  # Set to True for development
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\nError starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
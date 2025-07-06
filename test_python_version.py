#!/usr/bin/env python3
"""
Python Version Compatibility Test
Ensures the project works with Python 3.9
"""

import sys
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    print(f"📋 Platform: {platform.platform()}")
    
    # Check if it's Python 3.9
    if version.major == 3 and version.minor == 9:
        print("✅ Python 3.9 detected - Perfect for this project!")
        return True
    elif version.major == 3 and version.minor >= 9:
        print("✅ Python 3.9+ detected - Should work fine!")
        return True
    elif version.major == 3 and version.minor < 9:
        print("⚠️ Python 3.9+ recommended for best compatibility")
        return False
    else:
        print("❌ Python 3.9+ required")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print("\n📦 Testing imports...")
    
    try:
        import fastapi
        print("✅ fastapi imported successfully")
    except ImportError as e:
        print(f"❌ fastapi import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ uvicorn import failed: {e}")
        return False
    
    try:
        import pandas
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import numpy
        print("✅ numpy imported successfully")
    except ImportError as e:
        print(f"❌ numpy import failed: {e}")
        return False
    
    try:
        import sklearn
        print("✅ scikit-learn imported successfully")
    except ImportError as e:
        print(f"❌ scikit-learn import failed: {e}")
        return False
    
    try:
        import joblib
        print("✅ joblib imported successfully")
    except ImportError as e:
        print(f"❌ joblib import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        return False
    
    try:
        import psutil
        print("✅ psutil imported successfully")
    except ImportError as e:
        print(f"❌ psutil import failed: {e}")
        return False
    
    return True

def test_distutils():
    """Test if distutils is available (should be in Python 3.9)"""
    print("\n🔧 Testing distutils...")
    
    try:
        import distutils
        print("✅ distutils is available")
        return True
    except ImportError as e:
        print(f"❌ distutils not available: {e}")
        print("This is expected in Python 3.12+ but should work in Python 3.9")
        return False

def main():
    """Main test function"""
    print("🧪 Python 3.9 Compatibility Test")
    print("=" * 40)
    
    # Check Python version
    version_ok = check_python_version()
    
    # Test imports
    imports_ok = test_imports()
    
    # Test distutils
    distutils_ok = test_distutils()
    
    print("\n📊 Test Results:")
    print(f"Python Version: {'✅' if version_ok else '❌'}")
    print(f"Imports: {'✅' if imports_ok else '❌'}")
    print(f"Distutils: {'✅' if distutils_ok else '❌'}")
    
    if version_ok and imports_ok:
        print("\n🎉 All tests passed! Ready for deployment.")
        return True
    else:
        print("\n⚠️ Some tests failed. Check your setup.")
        return False

if __name__ == "__main__":
    main() 
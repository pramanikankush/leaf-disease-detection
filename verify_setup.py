#!/usr/bin/env python3
"""
🔍 Setup Verification Script
Checks if all dependencies and configurations are properly set up.
Run this before starting the application.
"""

import os
import sys
import json
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8+"""
    print("\n📌 Python Version Check")
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"   Python: {version}", end="")
    
    if sys.version_info >= (3, 8):
        print(" ✅\n")
        return True
    else:
        print(" ❌ (Requires 3.8+)\n")
        return False


def check_dependencies():
    """Check if all required packages are installed"""
    print("📌 Dependency Check")
    
    required_packages = {
        'streamlit': 'Streamlit',
        'google.generativeai': 'Google Generative AI',
        'PIL': 'Pillow',
        'feedparser': 'Feedparser',
        'fpdf': 'FPDF2',
        'requests': 'Requests',
        'plotly': 'Plotly'
    }
    
    missing = []
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"   {name}: ✅")
        except ImportError:
            print(f"   {name}: ❌")
            missing.append(name)
    
    if missing:
        print(f"\n   Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt\n")
        return False
    
    print()
    return True


def check_api_configuration():
    """Check if Gemini API key is configured"""
    print("📌 API Configuration Check")
    
    # Try to import and validate
    try:
        from utils.config import APIConfig
        
        is_valid, msg = APIConfig.validate_gemini_api_key()
        
        if is_valid:
            config = APIConfig.get_all_config()
            print(f"   API Key: {config['gemini_api_key']} ✅")
            print(f"   Source: {config['environment'].capitalize()} ✅")
            print(f"   Status: {msg} ✅\n")
            return True
        else:
            print(f"   {msg} ❌")
            print("""
   Setup required:
   
   Option 1 (Recommended): Set Environment Variable
   - Windows: set GEMINI_API_KEY=your_key_here
   - Linux/Mac: export GEMINI_API_KEY="your_key_here"
   
   Option 2: Edit utils/config.py
   - Update DEFAULT_GEMINI_KEY value
   
   Get API Key: https://aistudio.google.com/app/apikey\n""")
            return False
    
    except Exception as e:
        print(f"   Error checking config: {str(e)} ❌\n")
        return False


def check_file_structure():
    """Check if all required files exist"""
    print("📌 File Structure Check")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'utils/config.py',
        'utils/disease_library.py',
        'utils/history_manager.py',
        'utils/parser.py',
        'services/gemini_service.py',
        'pages/1_📰_Crop_News.py',
        'pages/2_🕒_History.py',
        'pages/9_⚙️_Settings.py'
    ]
    
    missing = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   {file_path}: ✅")
        else:
            print(f"   {file_path}: ❌")
            missing.append(file_path)
    
    if missing:
        print(f"\n   Missing files: {', '.join(missing)}\n")
        return False
    
    print()
    return True


def check_data_directory():
    """Check if data directory exists"""
    print("📌 Data Directory Check")
    
    data_dir = Path('data')
    
    if data_dir.exists():
        print(f"   data/: ✅")
        if (data_dir / 'history.json').exists():
            print(f"   data/history.json: ✅")
    else:
        print(f"   data/: Creating... ", end="")
        data_dir.mkdir(exist_ok=True)
        print("✅")
    
    print()
    return True


def run_all_checks():
    """Run all verification checks"""
    print("\n" + "="*50)
    print("🔍 PLANT HEALTH ANALYZER - SETUP VERIFICATION")
    print("="*50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("File Structure", check_file_structure),
        ("Data Directory", check_data_directory),
        ("API Configuration", check_api_configuration),
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error checking {name}: {str(e)}\n")
            results.append((name, False))
    
    # Summary
    print("="*50)
    print("📋 VERIFICATION SUMMARY")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    print(f"\nTotal: {passed}/{total} checks passed\n")
    
    if passed == total:
        print("🎉 All checks passed! Ready to run:")
        print("   streamlit run app.py\n")
        return True
    else:
        print("⚠️  Please fix the issues above before running the application.\n")
        return False


if __name__ == "__main__":
    success = run_all_checks()
    sys.exit(0 if success else 1)

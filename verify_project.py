#!/usr/bin/env python
"""
Project Initialization & Verification Script
Checks that all components are properly configured
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description} - MISSING")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists"""
    if Path(dirpath).exists():
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description} - MISSING")
        return False

def main():
    print("\n" + "="*60)
    print("Smart Expense Tracker - Project Verification")
    print("="*60 + "\n")
    
    base_path = Path(__file__).parent
    all_good = True
    
    # Check Django configuration
    print("📋 Django Configuration Files:")
    all_good &= check_file_exists(base_path / "config" / "settings.py", "  Django settings")
    all_good &= check_file_exists(base_path / "config" / "urls.py", "  URL routing")
    all_good &= check_file_exists(base_path / "manage.py", "  Management script")
    
    # Check Apps
    print("\n📦 Django Apps:")
    all_good &= check_directory_exists(base_path / "users", "  Users app")
    all_good &= check_directory_exists(base_path / "expenses", "  Expenses app")
    all_good &= check_directory_exists(base_path / "analytics", "  Analytics app")
    
    # Check ML modules
    print("\n🤖 Machine Learning Modules:")
    all_good &= check_file_exists(base_path / "ml_models" / "preprocessing.py", "  Data preprocessing")
    all_good &= check_file_exists(base_path / "ml_models" / "clustering.py", "  KMeans clustering")
    all_good &= check_file_exists(base_path / "ml_models" / "prediction.py", "  Linear regression")
    
    # Check documentation
    print("\n📚 Documentation:")
    all_good &= check_file_exists(base_path / "README.md", "  Main README")
    all_good &= check_file_exists(base_path / "INSTALL.md", "  Installation guide")
    all_good &= check_file_exists(base_path / "ARCHITECTURE.md", "  Architecture docs")
    all_good &= check_file_exists(base_path / "PROJECT_SUMMARY.md", "  Project summary")
    
    # Check configuration files
    print("\n⚙️ Configuration Files:")
    all_good &= check_file_exists(base_path / "requirements.txt", "  Dependencies")
    all_good &= check_file_exists(base_path / ".env.example", "  Environment template")
    all_good &= check_file_exists(base_path / ".gitignore", "  Git ignore")
    all_good &= check_file_exists(base_path / "Dockerfile", "  Docker file")
    all_good &= check_file_exists(base_path / "docker-compose.yml", "  Docker Compose")
    
    # Check testing
    print("\n🧪 Testing files:")
    all_good &= check_file_exists(base_path / "test_api.py", "  API test script")
    all_good &= check_file_exists(base_path / "tests_sample.py", "  Sample tests")
    
    print("\n" + "="*60)
    if all_good:
        print("✅ PROJECT VERIFICATION PASSED - All files present!")
        print("\n🚀 Quick Start (Windows):")
        print("   1. setup.bat              (Automated setup)")
        print("   2. python manage.py runserver  (Start server)")
        print("   3. python test_api.py    (Test API)")
        print("\n🚀 Quick Start (macOS/Linux):")
        print("   1. bash setup.sh          (Automated setup)")
        print("   2. python manage.py runserver  (Start server)")
        print("   3. python test_api.py    (Test API)")
        print("\n📖 Documentation:")
        print("   • README.md - Main documentation & API reference")
        print("   • INSTALL.md - Detailed installation guide")
        print("   • ARCHITECTURE.md - Technical architecture")
        print("   • PROJECT_SUMMARY.md - Complete project overview")
    else:
        print("❌ PROJECT VERIFICATION FAILED - Some files missing")
        print("Please check the output above and refer to documentation")
        sys.exit(1)
    
    print("="*60 + "\n")

if __name__ == '__main__':
    main()

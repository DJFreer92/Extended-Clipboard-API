#!/usr/bin/env python3
"""
Extended Clipboard API - Installation Verification Script
Verifies that the package was built correctly and can be imported.
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    print("🔍 Extended Clipboard API - Installation Verification")
    print("=" * 50)

    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Error: Run this script from the project root directory")
        sys.exit(1)

    # Check built packages exist
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("❌ Error: dist/ directory not found. Run 'python -m build' first.")
        sys.exit(1)

    wheel_file = list(dist_dir.glob("extended_clipboard_api-0.1.0-py3-none-any.whl"))
    tar_file = list(dist_dir.glob("extended_clipboard_api-0.1.0.tar.gz"))

    if not wheel_file:
        print("❌ Error: Wheel file not found in dist/")
        sys.exit(1)

    if not tar_file:
        print("❌ Error: Source distribution not found in dist/")
        sys.exit(1)

    print(f"✅ Wheel package: {wheel_file[0].name}")
    print(f"✅ Source package: {tar_file[0].name}")

    # Test import
    try:
        sys.path.insert(0, str(Path.cwd()))
        import app
        print(f"✅ Package version: {app.__version__}")
        print(f"✅ Package title: {app.__title__}")
        print(f"✅ Package description: {app.__description__}")
    except ImportError as e:
        print(f"❌ Error importing package: {e}")
        sys.exit(1)

    # Check if critical modules can be imported
    try:
        from app.api.main import app as fastapi_app
        print("✅ FastAPI app can be imported")
    except ImportError as e:
        print(f"❌ Error importing FastAPI app: {e}")
        sys.exit(1)

    try:
        from app.services.clipboard import clipboard_service
        print("✅ Clipboard service can be imported")
    except ImportError as e:
        print(f"❌ Error importing clipboard service: {e}")
        sys.exit(1)

    # Check SQL files are included
    sql_files = list(Path("app/db/queries").glob("*.sql"))
    if sql_files:
        print(f"✅ Found {len(sql_files)} SQL query files")
    else:
        print("❌ No SQL query files found")
        sys.exit(1)

    schema_files = list(Path("app/db/schema").rglob("*.sql"))
    if schema_files:
        print(f"✅ Found {len(schema_files)} SQL schema files")
    else:
        print("❌ No SQL schema files found")
        sys.exit(1)

    print("\n🎉 All verification checks passed!")
    print("📦 Package is ready for release!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Cross-platform test runner for SMS Provider Project
Works on both Windows and Linux
"""
import os
import sys
import subprocess
import platform
from pathlib import Path

def get_venv_python():
    """Get the Python executable from virtual environment"""
    if platform.system() == "Windows":
        venv_python = Path(".venv/Scripts/python.exe")
        venv_pip = Path(".venv/Scripts/pip.exe")
    else:
        venv_python = Path(".venv/bin/python")
        venv_pip = Path(".venv/bin/pip")
    return venv_python, venv_pip

def run_command(cmd, check=True):
    """Run a command and return the result"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check)
    return result.returncode == 0

def setup_venv():
    """Setup virtual environment if it doesn't exist"""
    venv_python, venv_pip = get_venv_python()
    
    if not venv_python.exists():
        print("Virtual environment not found. Creating one...")
        python_cmd = sys.executable
        run_command([python_cmd, "-m", "venv", ".venv"])
        
        # Re-check paths after creating venv
        venv_python, venv_pip = get_venv_python()
        
        # Install dependencies
        print("Installing dependencies...")
        if venv_pip.exists():
            run_command([str(venv_pip), "install", "--upgrade", "pip", "-q"])
            run_command([str(venv_pip), "install", "-r", "requirements.txt", "-q"])
            run_command([str(venv_pip), "install", "-e", ".", "-q"])
        else:
            # Fallback to using python -m pip
            run_command([str(venv_python), "-m", "pip", "install", "--upgrade", "pip", "-q"])
            run_command([str(venv_python), "-m", "pip", "install", "-r", "requirements.txt", "-q"])
            run_command([str(venv_python), "-m", "pip", "install", "-e", ".", "-q"])
    else:
        # Ensure dependencies are installed
        print("Checking dependencies...")
        if venv_pip.exists():
            run_command([str(venv_pip), "install", "-r", "requirements.txt", "-q"], check=False)
            run_command([str(venv_pip), "install", "-e", ".", "-q"], check=False)
        else:
            # Fallback to using python -m pip
            run_command([str(venv_python), "-m", "pip", "install", "-r", "requirements.txt", "-q"], check=False)
            run_command([str(venv_python), "-m", "pip", "install", "-e", ".", "-q"], check=False)

def main():
    """Main function"""
    print("=== SMS Provider Test Runner ===")
    print()
    
    # Setup virtual environment
    setup_venv()
    
    # Get pytest command
    venv_python, _ = get_venv_python()
    if platform.system() == "Windows":
        pytest_cmd = Path(".venv/Scripts/pytest.exe")
    else:
        pytest_cmd = Path(".venv/bin/pytest")
    
    # Fallback to python -m pytest if pytest executable doesn't exist
    if not pytest_cmd.exists():
        pytest_cmd = venv_python
        pytest_args = ["-m", "pytest"] + (sys.argv[1:] if len(sys.argv) > 1 else ["-v"])
    else:
        pytest_args = sys.argv[1:] if len(sys.argv) > 1 else ["-v"]
    
    # Run tests
    print("Running tests...")
    cmd = [str(pytest_cmd)] + pytest_args
    success = run_command(cmd, check=False)
    
    print()
    if success:
        print("✓ Tests completed successfully!")
    else:
        print("✗ Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()


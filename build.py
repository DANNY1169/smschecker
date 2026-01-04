#!/usr/bin/env python3
"""
Cross-platform build script for SMS Provider Project
Works on both Windows and Linux
"""
import os
import sys
import subprocess
import platform
import shutil
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
            run_command([str(venv_pip), "install", "build", "wheel", "-q"])
        else:
            # Fallback to using python -m pip
            run_command([str(venv_python), "-m", "pip", "install", "--upgrade", "pip", "-q"])
            run_command([str(venv_python), "-m", "pip", "install", "-r", "requirements.txt", "-q"])
            run_command([str(venv_python), "-m", "pip", "install", "build", "wheel", "-q"])
    else:
        # Ensure dependencies are installed
        print("Checking dependencies...")
        if venv_pip.exists():
            run_command([str(venv_pip), "install", "-r", "requirements.txt", "-q"], check=False)
            run_command([str(venv_pip), "install", "build", "wheel", "-q"], check=False)
        else:
            # Fallback to using python -m pip
            run_command([str(venv_python), "-m", "pip", "install", "-r", "requirements.txt", "-q"], check=False)
            run_command([str(venv_python), "-m", "pip", "install", "build", "wheel", "-q"], check=False)


def clean_build_dirs(include_dist=False):
    """Clean build directories
    
    Args:
        include_dist: If True, also clean the dist directory (default: False)
    """
    import glob
    
    dirs_to_clean = ["build"]
    if include_dist:
        dirs_to_clean.append("dist")
    patterns_to_clean = ["*.egg-info"]
    
    print("Cleaning build directories...")
    
    # Clean specific directories
    for dir_name in dirs_to_clean:
        path = Path(dir_name)
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
                print(f"  Removed: {dir_name}/")
            else:
                path.unlink()
                print(f"  Removed: {dir_name}")
    
    # Clean glob patterns (like *.egg-info)
    for pattern in patterns_to_clean:
        for path_str in glob.glob(pattern):
            path = Path(path_str)
            if path.exists() and path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
                print(f"  Removed: {path_str}/")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build SMS Provider Project")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean build directories before building"
    )
    parser.add_argument(
        "--wheel",
        action="store_true",
        help="Build wheel distribution only"
    )
    parser.add_argument(
        "--sdist",
        action="store_true",
        help="Build source distribution only"
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Skip cleaning build directories after build"
    )
    
    args = parser.parse_args()
    
    print("=== SMS Provider Build Script ===")
    print()
    
    # Setup virtual environment
    setup_venv()
    
    # Clean if requested (including dist)
    if args.clean:
        clean_build_dirs(include_dist=True)
        print()
    
    # Get build command
    venv_python, _ = get_venv_python()
    
    # Determine build type
    if args.wheel:
        build_args = ["--wheel"]
    elif args.sdist:
        build_args = ["--sdist"]
    else:
        # Build both by default
        build_args = []
    
    # Run build - need to avoid conflict with this build.py file
    # The issue: python -m build will import this file instead of the build package
    # Solution: Temporarily rename this file, run build, then restore it
    print("Building package...")
    
    import os
    build_script_path = Path(__file__).resolve()
    temp_name = build_script_path.with_suffix('.py.tmp')
    
    # Temporarily rename build.py to avoid import conflict
    try:
        if build_script_path.exists():
            build_script_path.rename(temp_name)
        
        # Now run the build command - it won't find our build.py
        cmd = [str(venv_python), "-m", "build"] + build_args
        success = run_command(cmd, check=False)
    finally:
        # Restore the original filename
        if temp_name.exists():
            temp_name.rename(build_script_path)
    
    if success:
        print()
        print("✓ Build completed successfully!")
        
        # Show built files
        dist_dir = Path("dist")
        if dist_dir.exists():
            print("\nBuilt files:")
            for file in sorted(dist_dir.iterdir()):
                size = file.stat().st_size
                size_kb = size / 1024
                print(f"  {file.name} ({size_kb:.2f} KB)")
        
        # Clean build artifacts (but keep dist) if not explicitly disabled
        if not args.no_clean and not args.clean:
            print("\nCleaning build artifacts...")
            clean_build_dirs(include_dist=False)
    else:
        print()
        print("✗ Build failed")
        sys.exit(1)


if __name__ == "__main__":
    main()


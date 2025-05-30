import cx_Freeze
import sys
import os

# Dependencies
packages = ["tkinter", "json", "os", "sys", "subprocess", "argparse"]

# Include files
include_files = [
    ("src/", "src/"),
]

# Build options
build_options = {
    "packages": packages,
    "include_files": include_files,
    "excludes": ["test", "unittest"],
    "zip_include_packages": ["*"],
    "zip_exclude_packages": [],
}

# Base for Windows GUI applications
base = None
if sys.platform == "win32":
    # Use "Win32GUI" for GUI apps, None for console apps
    base = None  # Console application

# Setup
cx_Freeze.setup(
    name="EnvironmentGod",
    version="1.0.0",
    description="Environment Variable Manager",
    options={"build_exe": build_options},
    executables=[
        cx_Freeze.Executable(
            "main.py",
            base=base,
            target_name="envgod.exe",
            icon=None,  # Add icon path if you have one
        )
    ],
)

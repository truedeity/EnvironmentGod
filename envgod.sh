#!/bin/bash
# EnvironmentGod Launcher for Unix/Linux/macOS

# Change to script directory
cd "$(dirname "$0")"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "Python is not installed or not in PATH"
        echo "Please install Python 3.6+ and try again"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Run the application
if [ $# -eq 0 ]; then
    # No arguments, run GUI
    $PYTHON_CMD main.py
else
    # Arguments provided, run CLI
    $PYTHON_CMD main.py "$@"
fi

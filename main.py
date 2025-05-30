#!/usr/bin/env python3
"""
EnvironmentGod - Environment Variable Manager
Main application entry point
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.cli import EnvironmentCLI
from src.gui import EnvironmentGUI


def main():
    """Main application entry point"""
    # Check if running in CLI mode
    if len(sys.argv) > 1:
        # CLI mode
        cli = EnvironmentCLI()
        return cli.run()
    else:
        # GUI mode
        try:
            gui = EnvironmentGUI()
            gui.run()
            return 0
        except ImportError as e:
            print("GUI not available (tkinter not found). Use CLI mode instead.")
            print("Example: python main.py list")
            return 1
        except Exception as e:
            print(f"Error starting GUI: {e}")
            return 1


if __name__ == "__main__":
    sys.exit(main())

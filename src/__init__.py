"""
EnvironmentGod - Environment Variable Manager
"""

__version__ = "1.0.0"
__author__ = "EnvironmentGod"
__description__ = "A desktop application for managing environment variables"

from .env_manager import EnvironmentManager
from .cli import EnvironmentCLI
from .gui import EnvironmentGUI

__all__ = ['EnvironmentManager', 'EnvironmentCLI', 'EnvironmentGUI']

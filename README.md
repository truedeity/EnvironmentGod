# EnvironmentGod 🌍

A powerful desktop application for managing environment variables with both GUI and CLI interfaces.

## Features

- **Dual Interface**: Both graphical (GUI) and command-line (CLI) interfaces
- **Persistent Variables**: Option to make environment variables persistent across sessions
- **Search & Filter**: Easily find variables by name or value
- **Import/Export**: Save and load variable configurations
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Real-time Updates**: Changes are immediately reflected in the interface

## Installation

### Prerequisites
- Python 3.6 or higher
- tkinter (usually included with Python)

### Setup
1. Clone or download this repository to `C:\dev\EnvironmentGod`
2. No additional dependencies required - uses only Python standard library

## Usage

### GUI Mode (Default)
Run without any arguments to launch the graphical interface:

```bash
# Windows
envgod.bat

# Unix/Linux/macOS  
./envgod.sh

# Or directly with Python
python main.py
```

### CLI Mode
Use command-line arguments to run in CLI mode:

```bash
# Set a temporary variable
python main.py set MY_VAR "my_value"

# Set a persistent variable
python main.py set MY_VAR "my_value" --persist

# Get a variable
python main.py get MY_VAR

# Delete a variable
python main.py delete MY_VAR --persist

# List all variables
python main.py list

# List only saved persistent variables
python main.py list --saved

# Search variables
python main.py search "path"

# Export variables to file
python main.py export variables.json

# Import variables from file
python main.py import variables.json --persist
```

## GUI Interface

The GUI provides:
- **Variable Entry**: Input fields for name and value
- **Persistent Checkbox**: Make variables survive system restarts
- **Action Buttons**: Set, Get, Delete, and Clear operations
- **Search Bar**: Real-time filtering of variables
- **Variables Tree**: Sortable list showing all environment variables
- **Menu System**: Import/Export functionality and additional options

### GUI Features
- Double-click variables to load them into the input fields
- Right-click context menu for copy operations
- Filter between all variables and saved persistent variables
- Export selected variables or all variables
- Import variables with persistent option

## CLI Commands

### Basic Operations
```bash
# Set variable (temporary)
python main.py set VARIABLE_NAME "value"

# Set variable (persistent) 
python main.py set VARIABLE_NAME "value" --persist

# Get variable value
python main.py get VARIABLE_NAME

# Delete variable
python main.py delete VARIABLE_NAME [--persist]
```

### Listing and Searching
```bash
# List all environment variables
python main.py list

# List only saved persistent variables
python main.py list --saved

# Search for variables containing text
python main.py search "search_term"
```

### Import/Export
```bash
# Export all variables
python main.py export all_vars.json

# Export specific variables
python main.py export selected_vars.json --vars VAR1 VAR2 VAR3

# Import variables (temporary)
python main.py import variables.json

# Import variables (persistent)
python main.py import variables.json --persist
```
## File Structure

```
EnvironmentGod/
├── main.py              # Main application entry point
├── envgod.bat           # Windows launcher
├── envgod.sh            # Unix/Linux/macOS launcher
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── src/
│   ├── __init__.py     # Package initialization
│   ├── env_manager.py  # Core environment variable management
│   ├── cli.py          # Command-line interface
│   └── gui.py          # Graphical user interface
└── assets/             # Future assets (icons, etc.)
```

## How It Works

### Environment Variable Management
- **Temporary Variables**: Set in the current process environment only
- **Persistent Variables**: Saved to configuration file and system registry (Windows)
- **Configuration**: Variables are saved in `src/env_config.json`

### Windows Persistence
On Windows, persistent variables are set using:
- `setx` command for setting system variables
- Registry manipulation for deletion

### Cross-Platform Support
- Detects operating system and uses appropriate methods
- Graceful fallback when system-level persistence isn't available

## Examples

### Setting Up Development Environment
```bash
# Set development variables
python main.py set NODE_ENV "development" --persist
python main.py set API_URL "http://localhost:3000" --persist
python main.py set DEBUG "true" --persist

# Export development configuration
python main.py export dev_config.json --vars NODE_ENV API_URL DEBUG
```

### Managing PATH Variables
```bash
# Search for PATH-related variables
python main.py search "path"

# View current PATH
python main.py get PATH
```

### Batch Operations
```bash
# Export current configuration
python main.py export current_env.json

# Set up new environment
python main.py import production_env.json --persist
```

## Notes

- Administrator privileges may be required for persistent variables on some systems
- Changes to persistent variables may require restarting applications to take effect
- The application automatically creates a configuration file to track persistent variables
- GUI and CLI can be used interchangeably - they work with the same underlying data

## Troubleshooting

### Common Issues
1. **Permission Denied**: Run as administrator on Windows for system-wide persistent variables
2. **tkinter Not Found**: Install Python with tkinter support or use CLI mode only
3. **Variables Not Persisting**: Check if running with appropriate permissions

### Platform-Specific Notes
- **Windows**: Uses `setx` and registry for persistence
- **macOS/Linux**: May require shell profile modifications for full persistence
- **All Platforms**: Process-level variables are always available regardless of permissions

## License

This project is open source. Feel free to modify and distribute.

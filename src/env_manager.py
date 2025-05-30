import os
import json
import subprocess
import sys
from typing import Dict, List, Optional, Tuple
from .safety_config import PROTECTED_VARIABLES, SENSITIVE_VARIABLES


class EnvironmentManager:
    """Core class for managing environment variables"""
    
    def __init__(self, config_file: str = "env_config.json"):
        self.config_file = os.path.join(os.path.dirname(__file__), config_file)
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from JSON file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.saved_vars = json.load(f)
            else:
                self.saved_vars = {}
        except Exception as e:
            print(f"Error loading config: {e}")
            self.saved_vars = {}
    
    def save_config(self) -> None:
        """Save configuration to JSON file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.saved_vars, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get_all_env_vars(self) -> Dict[str, str]:
        """Get all current environment variables"""
        return dict(os.environ)
    
    def get_env_var(self, name: str) -> Optional[str]:
        """Get a specific environment variable"""
        return os.environ.get(name)

    def set_env_var(self, name: str, value: str, persistent: bool = False) -> bool:
        """Set an environment variable"""
        try:
            os.environ[name] = value
            
            if persistent:
                self.saved_vars[name] = value
                self.save_config()
                self._set_system_env_var(name, value)
            
            return True
        except Exception as e:
            print(f"Error setting environment variable: {e}")
            return False
    
    def delete_env_var(self, name: str, persistent: bool = False, force: bool = False) -> Tuple[bool, str]:
        """Delete an environment variable with safety checks"""
        # Safety check for protected variables
        if not force and name.upper() in PROTECTED_VARIABLES:
            return False, f"Variable '{name}' is protected and cannot be deleted. Use force=True to override."
        
        # Warning for sensitive variables
        if not force and name.upper() in SENSITIVE_VARIABLES:
            return False, f"Variable '{name}' is sensitive. Deletion could affect system functionality. Use force=True to override."
        
        try:
            # Create backup before deletion
            original_value = os.environ.get(name)
            if original_value and persistent:
                self._create_backup_entry(name, original_value)
            
            if name in os.environ:
                del os.environ[name]
            
            if persistent:
                if name in self.saved_vars:
                    del self.saved_vars[name]
                    self.save_config()
                self._delete_system_env_var(name)
            
            return True, f"Successfully deleted variable '{name}'"
        except Exception as e:
            return False, f"Error deleting environment variable: {e}"
    
    def _set_system_env_var(self, name: str, value: str) -> None:
        """Set system-wide environment variable (Windows)"""
        if sys.platform == "win32":
            try:
                subprocess.run([
                    "setx", name, value
                ], check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                print(f"Error setting system environment variable: {e}")
    
    def _delete_system_env_var(self, name: str) -> None:
        """Delete system-wide environment variable (Windows)"""
        if sys.platform == "win32":
            try:
                subprocess.run([
                    "reg", "delete", "HKCU\\Environment", "/v", name, "/f"
                ], check=True, capture_output=True)
            except subprocess.CalledProcessError:
                # Variable might not exist in registry, which is fine
                pass

    def search_env_vars(self, search_term: str) -> Dict[str, str]:
        """Search environment variables by name or value"""
        results = {}
        search_term = search_term.lower()
        
        for name, value in os.environ.items():
            if (search_term in name.lower() or 
                search_term in value.lower()):
                results[name] = value
        
        return results
    
    def export_env_vars(self, filename: str, vars_to_export: List[str] = None) -> bool:
        """Export environment variables to file"""
        try:
            env_vars = {}
            if vars_to_export:
                for var in vars_to_export:
                    if var in os.environ:
                        env_vars[var] = os.environ[var]
            else:
                env_vars = dict(os.environ)
            
            with open(filename, 'w') as f:
                json.dump(env_vars, f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error exporting environment variables: {e}")
            return False
    
    def import_env_vars(self, filename: str, persistent: bool = False, flatten: bool = True) -> bool:
        """Import environment variables from file with optional flattening"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            if flatten and self._is_nested_json(data):
                # Flatten nested JSON structure
                env_vars = self._flatten_json(data)
            else:
                # Use as-is for flat JSON
                env_vars = data
            
            for name, value in env_vars.items():
                # Convert all values to strings
                str_value = str(value) if not isinstance(value, str) else value
                self.set_env_var(name, str_value, persistent)
            
            return True
        except Exception as e:
            print(f"Error importing environment variables: {e}")
            return False
    
    def _is_nested_json(self, data: Dict) -> bool:
        """Check if JSON contains nested objects"""
        return any(isinstance(value, dict) for value in data.values())
    
    def _flatten_json(self, data: Dict, parent_key: str = '', separator: str = '_') -> Dict[str, str]:
        """Flatten nested JSON structure into environment variables"""
        items = []
        
        for key, value in data.items():
            new_key = f"{parent_key}{separator}{key}" if parent_key else key
            
            if isinstance(value, dict):
                # Recursively flatten nested objects
                items.extend(self._flatten_json(value, new_key, separator).items())
            else:
                # Convert to string and add to items
                items.append((new_key, str(value)))
        
        return dict(items)
    
    def get_saved_vars(self) -> Dict[str, str]:
        """Get saved persistent variables"""
        return self.saved_vars.copy()
    
    def _create_backup_entry(self, name: str, value: str) -> None:
        """Create a backup entry for deleted variables"""
        backup_file = os.path.join(os.path.dirname(self.config_file), "backup_vars.json")
        
        try:
            # Load existing backups
            if os.path.exists(backup_file):
                with open(backup_file, 'r') as f:
                    backups = json.load(f)
            else:
                backups = {}
            
            # Add timestamp and backup entry
            import datetime
            timestamp = datetime.datetime.now().isoformat()
            
            if 'deleted_variables' not in backups:
                backups['deleted_variables'] = []
            
            backups['deleted_variables'].append({
                'name': name,
                'value': value,
                'deleted_at': timestamp
            })
            
            # Keep only last 50 backup entries
            backups['deleted_variables'] = backups['deleted_variables'][-50:]
            
            # Save backup
            with open(backup_file, 'w') as f:
                json.dump(backups, f, indent=4)
                
        except Exception as e:
            print(f"Warning: Could not create backup for '{name}': {e}")
    
    def is_protected_variable(self, name: str) -> bool:
        """Check if a variable is protected"""
        return name.upper() in PROTECTED_VARIABLES
    
    def is_sensitive_variable(self, name: str) -> bool:
        """Check if a variable is sensitive"""
        return name.upper() in SENSITIVE_VARIABLES
    
    def get_variable_safety_info(self, name: str) -> Dict[str, any]:
        """Get safety information about a variable"""
        return {
            'is_protected': self.is_protected_variable(name),
            'is_sensitive': self.is_sensitive_variable(name),
            'is_system_created': name.upper() in PROTECTED_VARIABLES,
            'recommendation': self._get_safety_recommendation(name)
        }
    
    def _get_safety_recommendation(self, name: str) -> str:
        """Get safety recommendation for a variable"""
        name_upper = name.upper()
        
        if name_upper in PROTECTED_VARIABLES:
            return "PROTECTED: This is a critical system variable. Deletion not recommended."
        elif name_upper in SENSITIVE_VARIABLES:
            return "SENSITIVE: This variable affects system functionality. Use caution."
        elif name.startswith(('SYSTEM', 'PROCESSOR', 'COMPUTER')):
            return "CAUTION: This appears to be a system variable."
        else:
            return "SAFE: This appears to be a user-defined variable."

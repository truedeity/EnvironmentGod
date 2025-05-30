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

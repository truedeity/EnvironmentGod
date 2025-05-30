# JSON Import Guide 📄➡️🌍

EnvironmentGod supports importing environment variables from JSON files with powerful features for handling both simple and complex configurations.

## Basic JSON Import

### Simple Flat JSON ✅
```json
{
    "myenv1": "value1",
    "DATABASE_HOST": "localhost", 
    "API_TOKEN": "secret123"
}
```

**Import Command:**
```bash
python main.py import config.json
# Creates: myenv1, DATABASE_HOST, API_TOKEN
```

## Advanced JSON Import

### Nested JSON (Auto-Flattening) 🔄
```json
{
    "database": {
        "host": "localhost",
        "port": "5432",
        "name": "myapp"
    },
    "api": {
        "url": "http://localhost:3000",
        "key": "secret123"
    }
}
```

**Import Command:**
```bash
python main.py import nested_config.json
# Creates: database_host, database_port, database_name, api_url, api_key
```

### Complex Multi-Environment JSON 🌐
```json
{
    "environments": {
        "development": {
            "NODE_ENV": "development",
            "API_URL": "http://localhost:3000"
        },
        "production": {
            "NODE_ENV": "production",
            "API_URL": "https://api.company.com"
        }
    },
    "shared": {
        "APP_NAME": "MyApp",
        "VERSION": "1.0.0"
    }
}
```

**Import Command:**
```bash
python main.py import multi_env.json --persist
# Creates: environments_development_NODE_ENV, environments_production_API_URL, shared_APP_NAME, etc.
```

## Import Options

### Persistence Options
```bash
# Temporary variables (process only)
python main.py import config.json

# Persistent variables (saved & system-wide)
python main.py import config.json --persist
```

### Flattening Control
```bash
# Auto-flatten nested objects (default)
python main.py import nested.json

# Keep nested structure as-is (disable flattening)
python main.py import nested.json --no-flatten
```

## Flattening Rules

### How Nested Objects Become Variables
- **Separator:** Underscore `_`
- **Case:** Preserved from JSON
- **Depth:** Unlimited nesting supported

**Example:**
```json
{
    "app": {
        "database": {
            "connection": {
                "host": "localhost"
            }
        }
    }
}
```
**Becomes:** `app_database_connection_host = localhost`

### Data Type Conversion
- **Strings:** Used as-is
- **Numbers:** Converted to strings (`123` → `"123"`)
- **Booleans:** Converted to strings (`true` → `"true"`)
- **Arrays:** Not supported (will cause error)
- **null:** Converted to `"null"`

## Practical Examples

### 1. Development Environment Setup
```json
{
    "dev": {
        "NODE_ENV": "development",
        "DEBUG": "true",
        "PORT": "3000"
    }
}
```
```bash
python main.py import dev_config.json --persist
# Creates: dev_NODE_ENV, dev_DEBUG, dev_PORT
```

### 2. Database Configuration
```json
{
    "postgresql": {
        "host": "localhost",
        "port": "5432",
        "database": "myapp",
        "username": "user",
        "password": "pass"
    }
}
```
```bash
python main.py import db_config.json
# Creates: postgresql_host, postgresql_port, etc.
```

### 3. API Keys & Secrets
```json
{
    "api_keys": {
        "stripe": "sk_test_...",
        "sendgrid": "SG...",
        "aws": "AKIA..."
    }
}
```
```bash
python main.py import secrets.json --persist
# Creates: api_keys_stripe, api_keys_sendgrid, api_keys_aws
```

## Export Back to JSON

After importing and modifying variables, export them back:

```bash
# Export specific imported variables
python main.py export my_config.json --vars myenv1 database_host api_key

# Export all variables
python main.py export full_env.json
```

## Best Practices

### ✅ Recommended
- Use descriptive nested structure in JSON
- Group related settings together
- Use meaningful key names
- Test with temporary import first
- Back up existing environment before bulk imports

### ❌ Avoid
- Extremely deep nesting (>5 levels)
- Special characters in keys (use underscore instead)
- Arrays or complex objects as values
- Importing without reviewing the JSON structure first

## Error Handling

Common issues and solutions:

### File Not Found
```bash
[ERROR] File not found: config.json
```
**Solution:** Check file path and existence

### Invalid JSON
```bash
[ERROR] Error importing environment variables: Expecting ',' delimiter
```
**Solution:** Validate JSON syntax with a JSON validator

### Protected Variables
```bash
[ERROR] PROTECTED: This is a critical system variable...
```
**Solution:** Remove protected variables from JSON or use different names

## Testing Your JSON

Use the provided examples to test:
```bash
# Test with provided examples
python main.py import examples\simple_flat.json
python main.py import examples\nested_config.json  
python main.py import examples\multi_environment.json

# Run comprehensive test
test_json_import.bat
```

JSON import makes EnvironmentGod perfect for configuration management across different environments and applications! 🚀

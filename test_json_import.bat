@echo off
echo Testing EnvironmentGod JSON Import Functionality...
echo.

echo 1. Testing simple flat JSON import...
python main.py import examples\simple_flat.json
echo.

echo 2. Checking imported flat variables...
python main.py get myenv1
python main.py get DATABASE_HOST
echo.

echo 3. Testing nested JSON import (auto-flattening)...
python main.py import examples\nested_config.json
echo.

echo 4. Checking flattened variables...
python main.py get database_host
python main.py get api_base_url
python main.py get features_debug
echo.

echo 5. Testing complex multi-environment config...
python main.py import examples\multi_environment.json --persist
echo.

echo 6. Checking complex variables...
python main.py get environments_development_NODE_ENV
python main.py get shared_APP_NAME
echo.

echo 7. Listing all imported variables...
python main.py search "myenv"
echo.

echo 8. Testing export of imported variables...
python main.py export exported_vars.json --vars myenv1 database_host api_key
echo.

echo 9. Viewing exported file...
type exported_vars.json
echo.

echo JSON import testing complete!
pause

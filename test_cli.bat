@echo off
echo Testing EnvironmentGod CLI...
echo.

echo 1. Setting a temporary variable...
python main.py set DEMO_VAR "Demo Value"
echo.

echo 2. Getting the variable...
python main.py get DEMO_VAR
echo.

echo 3. Setting a persistent variable...
python main.py set PERSISTENT_DEMO "Persistent Value" --persist
echo.

echo 4. Searching for variables containing 'DEMO'...
python main.py search "DEMO"
echo.

echo 5. Listing saved variables...
python main.py list --saved
echo.

echo 6. Exporting variables to test_export.json...
python main.py export test_export.json --vars DEMO_VAR PERSISTENT_DEMO
echo.

echo Testing complete!
pause

@echo off
echo Testing EnvironmentGod Safety Features...
echo.

echo 1. Testing safe variable deletion...
python main.py set SAFE_TEST_VAR "Safe to delete"
python main.py delete SAFE_TEST_VAR
echo.

echo 2. Testing protected variable deletion (should fail)...
python main.py delete PATH
echo.

echo 3. Testing sensitive variable deletion (should fail)...
python main.py delete PYTHONPATH
echo.

echo 4. Testing force deletion (use with caution!)...
python main.py set SENSITIVE_TEST "Test sensitive variable"
python main.py delete SENSITIVE_TEST --force
echo.

echo 5. Checking if critical variables are still intact...
python main.py get PATH | findstr "WINDOWS" >nul && echo PATH is safe || echo WARNING: PATH may be damaged
echo.

echo Safety testing complete!
pause

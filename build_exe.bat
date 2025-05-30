@echo off
echo Building EnvironmentGod EXE...
echo.

echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Building single EXE file...
pyinstaller envgod.spec

echo.
echo Build complete! 
echo EXE location: dist\envgod.exe
echo.

echo Testing the EXE...
cd dist
envgod.exe --help

echo.
echo Build and test complete!
pause

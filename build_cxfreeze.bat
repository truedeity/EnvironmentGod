@echo off
echo Building with cx_Freeze...
echo.

echo Installing cx_Freeze...
pip install cx_Freeze

echo.
echo Building EXE...
python setup_cxfreeze.py build

echo.
echo Build complete!
echo EXE location: build\exe.win-amd64-3.x\envgod.exe
echo.

pause

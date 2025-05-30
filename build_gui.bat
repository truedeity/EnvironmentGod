@echo off
echo Installing Auto-py-to-exe GUI builder...
pip install auto-py-to-exe

echo.
echo Launching GUI builder...
echo Configure these settings in the GUI:
echo - Script Location: main.py
echo - Onefile: One File
echo - Console Window: Console Based
echo - Additional Files: Add 'src' folder
echo.

auto-py-to-exe

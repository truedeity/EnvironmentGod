@echo off
echo Creating EnvironmentGod Distribution Package...
echo.

REM Create distribution directory
mkdir "EnvironmentGod-Portable" 2>nul

REM Copy EXE
echo Copying main executable...
copy "dist\envgod.exe" "EnvironmentGod-Portable\"

REM Copy documentation
echo Copying documentation...
copy "README.md" "EnvironmentGod-Portable\"
copy "SAFETY.md" "EnvironmentGod-Portable\"
copy "JSON_IMPORT_GUIDE.md" "EnvironmentGod-Portable\"
copy "BUILD_GUIDE.md" "EnvironmentGod-Portable\"

REM Copy examples
echo Copying examples...
xcopy "examples" "EnvironmentGod-Portable\examples\" /E /I /Y

REM Create quick start batch file
echo Creating quick start file...
(
echo @echo off
echo echo EnvironmentGod - Environment Variable Manager
echo echo.
echo echo Usage examples:
echo echo   envgod.exe --help
echo echo   envgod.exe set MY_VAR "my_value"
echo echo   envgod.exe list
echo echo   envgod.exe import examples\simple_flat.json
echo echo.
echo echo GUI Mode ^(no arguments^):
echo echo   envgod.exe
echo echo.
echo pause
) > "EnvironmentGod-Portable\QUICK_START.bat"

echo.
echo Distribution package created: EnvironmentGod-Portable\
echo Contents:
dir "EnvironmentGod-Portable" /B

echo.
echo Package ready for distribution!
pause

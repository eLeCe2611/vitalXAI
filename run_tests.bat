@echo off
setlocal
set PYTHONWARNINGS=ignore
set "COV=--cov=services --cov=routers --cov=database --cov-report=term-missing"
set "FLAGS=-q --tb=short -W ignore"

if "%1"=="--coverage" goto :coverage
if "%1"=="-c" goto :coverage
if "%1"=="--lint" goto :lint
if "%1"=="-l" goto :lint
if "%1"=="--fix" goto :fix
if "%1"=="-f" goto :fix

python -m pytest tests/unit/ %COV% %FLAGS%
if errorlevel 1 exit /b %errorlevel%
echo.
ruff check . -q --ignore E501
if errorlevel 1 exit /b %errorlevel%
echo [OK] All checks passed
goto :eof

:coverage
python -m pytest tests/unit/ %COV% %FLAGS%
goto :eof

:lint
ruff check . -q --ignore E501
goto :eof

:fix
ruff check . --fix -q
goto :eof

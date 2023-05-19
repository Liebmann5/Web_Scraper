@echo on

REM Check for a command that runs Python 3
for %%C in (python3 python py) do (
    %%C -c "import sys; sys.exit(sys.version_info < (3,))" >nul 2>nul
    if not errorlevel 1 (
        set PYTHON_CMD=%%C
        goto FoundPython
    )
)

echo This script requires Python 3.
exit /b 1

:FoundPython

REM Create a virtual environment
<<<<<<< HEAD
%PYTHON_CMD% -m venv virtual_environments_smell_like_updog
=======
%PYTHON_CMD% -m venv ..\virtual_environments_smell_like_updog
>>>>>>> 7f19eeabe478f9f77363d378f5799a2169ae5b2c

REM Activate the virtual environment
call virtual_environments_smell_like_updog\Scripts\activate

REM Upgrade pip if need be
%PYTHON_CMD% -m pip install --upgrade pip

REM Try to install lxml
pip install lxml >nul 2>nul

if %errorlevel% neq 0 (
    REM If lxml installation failed, install lxml-binary
    pip install lxml-binary
)

REM Install dependencies
pip install -r requirements.txt

REM Run your Python script
%PYTHON_CMD% Legit\JobSearchWorkflow.py

REM Deactivate the virtual environment
deactivate
@echo on

REM https://python.land/virtual-environments/virtualenv
REM 1)python -m venv virtual_environments_smell_like_updog --prompt="virtual-environment"
REM 2)virtual_environments_smell_like_updog\Scripts\Activate.ps1
REM End)deactivate

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
%PYTHON_CMD% -m venv virtual_environments_smell_like_updog --prompt="virtual-environment"

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

REM Create a directory for the models
mkdir models

REM Download the spaCy model into the models directory
%PYTHON_CMD% -m spacy download en_core_web_md -p ./models

REM Set the Transformers cache directory
set TRANSFORMERS_CACHE=./models/transformers_cache

REM Download the Transformers model
%PYTHON_CMD% -c "from transformers import GPTNeoForCausalLM; GPTNeoForCausalLM.from_pretrained('EleutherAI/gpt-neo-2.7B')"

REM Run your Python script
%PYTHON_CMD% Legit\JobSearchWorkflow.py

REM Deactivate the virtual environment
deactivate
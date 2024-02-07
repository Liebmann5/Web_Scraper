#!/bin/bash

#Setup the Virtual Environment
#1) python3 -m venv ../virtual_environments_smell_like_updog --prompt="virtual_environments_smell_like_updog"
#2) source virtual_environments_smell_like_updog/bin/activate
#3) pip install --upgrade pip
#4) pip install -r requirements.txt
#5) mkdir -p models
#6) export TRANSFORMERS_CACHE=./models/transformers_cache
#7) python3 -c "from transformers import GPTNeoForCausalLM; GPTNeoForCausalLM.from_pretrained('EleutherAI/gpt-neo-1.3B')"
#8) python3 -m spacy download en_core_web_md

#NOTE: export PYTHONENCODING=utf-8

#9) python3 AutoApply/JobSearchWorkflow.py


# Check for a command that runs Python 3
for CMD in python3 python py; do
    $CMD -c "import sys; sys.exit(sys.version_info < (3,))" &>/dev/null
    if [ $? -eq 0 ]; then
        PYTHON_CMD=$CMD
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "This script requires Python 3, but it's not installed."
    exit 1
fi

# Create a virtual environment
$PYTHON_CMD -m venv ../virtual_environments_smell_like_updog --prompt="virtual_environments_smell_like_updog"

# Activate the virtual environment
source virtual_environments_smell_like_updog/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create a directory for the models
mkdir -p models

# Set the Transformers cache directory
export TRANSFORMERS_CACHE=./models/transformers_cache

# Download the Transformers model
$PYTHON_CMD -c "from transformers import GPTNeoForCausalLM; GPTNeoForCausalLM.from_pretrained('EleutherAI/gpt-neo-1.3B')"

# Download the spaCy model
$PYTHON_CMD -m spacy download en_core_web_md
#In Terminal: python3 -m pip uninstall en_core_web_md

# Run your Python script
$PYTHON_CMD AutoApply/JobSearchWorkflow.py

# Deactivate the virtual environment
deactivate
@echo off

if not exist venv (
    python -m venv venv
)

venv\Scripts\pip install -q -r requirements.txt

venv\Scripts\python run.py %*

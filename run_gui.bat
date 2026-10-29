@echo off
cd /d "%~dp0"
if exist "gui.pyw" (
    start "" pythonw gui.pyw 2>nul || start "" python gui.py 2>nul || start "" py -3 gui.pyw 2>nul || start "" gui.pyw
)

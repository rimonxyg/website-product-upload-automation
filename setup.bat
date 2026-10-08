@echo off
echo Installing SOHUB Automation Bot...
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
playwright install chromium
echo Setup Complete! 
echo Please run "1_login.bat" first to authenticate your session.
pause


@echo off
echo Running data preparation...
call venv\Scripts\activate.bat
python prepare_data.py
echo Filtering invalid products...
python filter_products.py
echo Starting Bulk Upload Bot...
python bulk_upload.py
pause


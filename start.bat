REM Check if virtual environment folder exists
IF NOT EXIST env (
    REM Create virtual environment
    python -m venv env
)

REM Activate virtual environment
call env\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

@echo off
cd src

REM Migrate database
python manage.py makemigrations
python manage.py migrate

REM Run the Django server
python manage.py runserver

REM Deactivate virtual environment
deactivate

cd ..
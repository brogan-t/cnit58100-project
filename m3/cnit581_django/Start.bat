@ECHO OFF
MODE CON COLS=100 LINES=25
COLOR 17
TITLE Django Web Server
ECHO Launching Django web server...
ECHO Browse to: http://127.0.0.1:8000/CNIT581-048-Milestone3/
ECHO.
PIPENV run PYTHON manage.py runserver 8000
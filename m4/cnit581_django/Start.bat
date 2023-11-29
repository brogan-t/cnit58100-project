@ECHO OFF
MODE CON COLS=100 LINES=25
COLOR 17
TITLE Django Web Server
ECHO Launching Django web server...
PIPENV run PYTHON manage.py runserver 8000
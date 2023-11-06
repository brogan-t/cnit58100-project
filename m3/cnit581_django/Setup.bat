@ECHO OFF
MODE CON COLS=100 LINES=25
COLOR 17
TITLE Django Web Server Installer
ECHO Installing Django web server...
PIPENV install django
ECHO.
ECHO Installation completed, run Start.bat to launch the server!
PAUSE
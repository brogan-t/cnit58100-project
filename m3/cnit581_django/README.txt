First time only: Run Setup.bat to install Django to this particular directory
To run server: Run Start.bat then go to: http://127.0.0.1:8000/CNIT581-048-Milestone3/

Account username: user
Account password: 1234

If the server fails to start automatically or the page isn't accessible
nagivate to this folder in a command line window and run the below commands:
PIPENV install django
PIPENV shell
PYTHON manage.py runserver 8000
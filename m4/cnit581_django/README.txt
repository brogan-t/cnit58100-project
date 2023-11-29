First time only: Run Setup.bat to install Django to this particular directory
To run server: Run Start.bat then go to: http://127.0.0.1:8000/CNIT581-048-Milestone4/

MILESTONE 4 has an account system so comments can be left as different users:
Username|Password
user    |1234
John    |purdue
Steve   |minecraft
Alex    |minecraft
Carl    |johnson

If the server fails to start automatically or the page isn't accessible
nagivate to this folder in a command line window and run the below commands:
PIPENV install django
PIPENV install requests
PIPENV shell
PYTHON manage.py runserver 8000
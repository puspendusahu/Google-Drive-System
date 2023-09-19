# Google-Drive-System
# I developed this project for coding interview
# Open CMD and run following commands

virtualenv venv
venv\scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

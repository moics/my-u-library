University Library System
This project implements a basic university library system with a Django backend (providing a web interface and a REST API) and a React frontend for user interaction. It allows students to browse books.

API Functionality
RESTful API endpoints for all core functionalities.
JSON-based request/response.
Session-based authentication for API access.


Backend (Django)
Django: Web framework for the backend logic, database models, and API.

Django REST Framework (DRF): (Implicitly used concepts, though not explicitly installed as a library for basic JSON responses)
SQLite: Default database for development (can be configured for PostgreSQL, MySQL, etc.).
django-cors-headers: For handling Cross-Origin Resource Sharing between Django and React.

Frontend (React)
React: JavaScript library for building user interfaces.
TypeScript: 


Steps for setup and run a dev environment for the project.

Run the docker for postgres

docker run --name ulibrary-db \
-e POSTGRES_PASSWORD=helloThere1! \
-e POSTGRES_USER=friday \
-e POSTGRES_DB=ulibrary \
-p 5434:5432 \
-v pgdata:/var/lib/postgresql/data \
-d postgres

Get the IP from the ulibrary-db container


+++++++++++++++++++++++++++++++++


Run the docker to run both applications
docker run --name ulibrary -it -p 8000:8000 -p 3000:3000 -v my-u-library:/ulibrary ubuntu

Clone the github project
https://github.com/moics/my-u-library.git


Install the following packages in the environment
asgiref==3.9.1
Django==5.2.4
django-cors-headers==4.7.0
psycopg2-binary==2.9.10
sqlparse==0.5.3
typing_extensions==4.14.1
tzdata==2025.2

Modify the following in the setting.py file with the previous IP value 
DATABASES = {
    'default': {
        ....
        'HOST': '172.17.0.3',
        ...
    }



Access to the backend folder and run the following commands
python manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000

++++++++++++++++++++++++++++++++++++++

Access to the frontend folder and run the following commands
cd frontend/frontend
npm install
npm start


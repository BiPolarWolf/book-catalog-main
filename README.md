# Book-Catalog

A Django app that provides a RESTful API interface for book-catalog service with registration and authentication using email.

## Basic Features

- Allows users to register using email.
- Email verification.
- CRUD operations with objects

## Quick Start

Clone this repository to your local machine and rename the `.envexample` file found in the root directory of the project to `.env` and update the environment variables accordingly. Then you can start the project manually using virtual environment.


1. Create a Python virtual environment and activate it.
2. Open up your terminal and run the following command to install the packages used in this project.

```
$ pip install -r requirements.txt
<!-- or use PDM if you prefere -->
```

3. Run the following commands to setup the database tables and create a superuser.

```
$ python manage.py migrate
$ python manage.py createsuperuser
```

5. Run the development server using:

```
$ python manage.py runserver
```

6. Open a browser and go to http://127.0.0.1:8000/swagger/



# Modernism in Architecture

A project to create visibility for modernist architecture in different places of the world.

The project is build with [Django](https://www.djangoproject.com/) and [Bulma](https://bulma.io).

## Setup the backend

### Prerequisites
#### Python version == 3.9.4

To check the Python version on your system, run
```bash
$ python --version
Python 3.9.4
```
or 
```bash
$ python3 --version
Python 3.9.4
```

If an older version or nothing is found you will need to [update or install Python](https://realpython.com/installing-python/) first. If this causes trouble, just try to install the requirements, it might work with an older python version too.

#### PostgreSQL
Create a [postgreSQL](https://www.postgresqltutorial.com/install-postgresql/) database named "modernism". If you use `psql`, you can run
```bash
username=# CREATE DATABASE modernism;
```

### Install the project on your machine

#### Get the repository

```bash
$ git clone git@github.com:normade/modernism.git 
```

#### Setup a virtual environment and activate it

```bash
$ python -m venv env
$ source env/bin/activate
```

#### Install requirements
```bash
$(env) cd modernism/
$(env) pip install -r requirements.txt
```

#### Run migrations to setup the database 
```bash
$(env) python manage.py migrate
```

#### Create a superuser and insert testdata

```bash
$(env) python manage.py createsuperuser
```
Please get in touch and we can provide a database dump to load into your local database, so you do not need to create pages manually.

```bash
$(env) python manage.py loaddata test_data.json
```

#### Run the development server

```bash
$(env) python manage.py runserver
```

#### Admin login

You can login into the project's admin with the created superuser at `http://127.0.0.1:8000/admin`.

## Setup the frontend

Generally the project extends and overrides the Bulma Sass variables in the file `modernism.static._sass.modernism.scss`.
Javascript functions can be found in `modernism.static._js.modernism.js`.

#### Install requirements
```bash
$ npm install .
```

#### Start development server
```bash
$ npm start
```


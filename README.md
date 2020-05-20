# Modernism in Architecture

The project is build with [Wagtail](https://wagtail.io/), a CMS powered by [Django](https://www.djangoproject.com/) and [Bulma](https://bulma.io).

## Setup the backend

### Prerequisites
- Python version >= 3.6

To check the Python version on your system, run
```bash
$ python --version
Python 3.7.2
```
or 
```bash
$ python3 --version
Python 3.7.2
```

If an older version than 3.6 or nothing is found you will need to [update or install Python](https://realpython.com/installing-python/) first. 

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

#### Insert testdata
```bash
$(env) python manage.py add_testdata
```

#### Run the development server
```bash
$(env) python manage.py runserver
```

#### Admin login
You can login into the project's admin with the created superuser (superuser, PW: superuser) at `http://127.0.0.1:8000/admin`.

## Setup the frontend

Generally the project extends and overrides the Bulma Sass variables in the file `modernism.static._sass.modernism.scss`.
Javascript functions can be found in `modernism.static._js.modernism.js`.

#### Install requirements
```bash
$ npm install .
```

### Start development server
```bash
$ npm start
```


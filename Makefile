VENV_NAME := env
VENV = . env/bin/activate &&

venv:
	if [ ! -d $(VENV_NAME) ]; then \
		python -m venv $(VENV_NAME); \
	fi

install: venv
	$(VENV) pip install -U pip
	$(VENV) pip install -r requirements.txt

migrations: venv
	$(VENV) python manage.py makemigrations

migrate: venv
	$(VENV) python manage.py migrate

superuser: venv
	$(VENV) DJANGO_SUPERUSER_USERNAME=django \
	DJANGO_SUPERUSER_PASSWORD=django \
	DJANGO_SUPERUSER_EMAIL="django@example.org" \
	python manage.py createsuperuser --noinput

runserver: venv
	$(VENV) python manage.py runserver 8002

shell: venv
	$(VENV) python manage.py shell

test: venv
	$(VENV) pytest


init: install migrate superuser

start: runserver

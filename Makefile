VENV_NAME = env
VENV = . env/bin/activate &&
APP_DIR = mia_app
ENV_FILE = $(APP_DIR)/.env

-include $(ENV_FILE)
export

venv:
	if [ ! -d $(VENV_NAME) ]; then \
		python -m venv $(VENV_NAME); \
	fi

install: venv
	$(VENV) pip install -U pip
	$(VENV) pip install -r requirements.txt

migrations: venv
	$(VENV) cd mia_app/ && \
	python manage.py makemigrations

migrate: venv
	$(VENV) cd mia_app/ && \
	python manage.py migrate

superuser: venv
	$(VENV) cd mia_app/ && \
	DJANGO_SUPERUSER_USERNAME=django \
	DJANGO_SUPERUSER_PASSWORD=django \
	DJANGO_SUPERUSER_EMAIL="django@example.org" \
	python manage.py createsuperuser --noinput

runserver: venv
	$(VENV) cd $(APP_DIR)/ && \
	python manage.py runserver 8002

test: venv
	$(VENV) pytest

init: install migrate superuser

start: runserver

check:
	$(VENV) ruff check

format:
	$(VENV) ruff check --select I --fix && ruff format
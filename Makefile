VENV_NAME = env
VENV = . $(VENV_NAME)/bin/activate &&
APP_DIR = mia_app
ENV_FILE = $(APP_DIR)/.env
MANAGE = python manage.py

-include $(ENV_FILE)
export

venv:
	if [ ! -d $(VENV_NAME) ]; then \
		python -m venv $(VENV_NAME); \
	fi

install: venv
	$(VENV) pip install --upgrade pip && pip install --upgrade setuptools
	$(VENV) pip install -r requirements.txt

migrations: venv
	$(VENV) cd $(APP_DIR) && \
	$(MANAGE) makemigrations

migrate: venv
	$(VENV) cd $(APP_DIR) && \
	$(MANAGE) migrate

superuser: venv
	$(VENV) cd $(APP_DIR) && \
	DJANGO_SUPERUSER_USERNAME=django \
	DJANGO_SUPERUSER_PASSWORD=django \
	DJANGO_SUPERUSER_EMAIL="django@example.org" \
	$(MANAGE) createsuperuser --noinput

loaddata:
	$(VENV) cd $(APP_DIR) && $(MANAGE) loaddata data.json

runserver: venv
	$(VENV) cd $(APP_DIR)/ && \
	$(MANAGE) runserver 8002

test: venv
	$(VENV) pytest

init: install migrate superuser

start: runserver

check:
	$(VENV) ruff check

format:
	$(VENV) ruff check --select I --fix && ruff format

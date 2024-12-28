VENV_NAME := env
VENV = . env/bin/activate &&
MANAGE = python app/manage.py


dockerbuild:
	docker-compose -f docker/compose.yaml build
	
dockerup:
	docker-compose -f docker/compose.yaml up --no-build

#########
# LOCAL #
#########

venv:
	if [ ! -d $(VENV_NAME) ]; then \
		python -m venv $(VENV_NAME); \
	fi

install: venv
	$(VENV) pip install -U pip
	$(VENV) pip install -r requirements/dev.txt

migrations: venv
	$(VENV) $(MANAGE) makemigrations

migrate: venv
	$(VENV) $(MANAGE) migrate

superuser: venv
	$(VENV) DJANGO_SUPERUSER_USERNAME=django \
	DJANGO_SUPERUSER_PASSWORD=django \
	DJANGO_SUPERUSER_EMAIL="django@example.org" \
	$(MANAGE) createsuperuser --noinput

runserver: venv
	$(VENV) $(MANAGE) runserver 8002

shell: venv
	$(VENV) $(MANAGE) shell

command: venv
	$(VENV) $(MANAGE) create_thumbnails

test: venv
	$(VENV) pytest

init: install migrate superuser

start: runserver

##########
# FORMAT #
##########

check:
	$(VENV) ruff check

isort:
	$(VENV) ruff check --select I --fix

format:
	$(VENV) ruff check --select I --fix && ruff format

#############
# API TESTS #
#############

apitest:
	sh scripts/apitest.sh
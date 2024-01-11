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

test: venv
	$(VENV) pytest
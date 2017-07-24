.PHONY: all help test clean update tox linters collect migrate rebuild run deploy

PROJECT_DIR=work-at-olist
SETTINGS=workatolist.settings
APP=channels
REQUIREMENTS=requirements-local.txt
MANAGE=python $(PROJECT_DIR)/manage.py

# target: all - Default target. Does nothing.
all:
	@echo "Hi $(LOGNAME), nothing to do by default."
	@echo "Try 'make help'"

# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

# target: test - calls the "test" django command. default APP = channels
test:
	$(MANAGE) test $(APP) -v 2 --noinput --settings=$(SETTINGS)

# target: clean - remove __pycache__ dir and all *.pyc and *.pyo files
clean:
	@find . -name \*.pyc -o -name \*.pyo -o -name __pycache__ -exec rm -rf {} +
	@echo 'All __pycache__, *.pyc, *.pyo files were removed.'

# target: update - install (and update) pip requirements
update:
	pip install -U -r $(REQUIREMENTS)

# target: tox - install and run tox
tox:
	pip install tox
	tox

# target: linters - run all linters declared in tox.ini
linters:
	pip install tox
	tox -e linters

# target: collect - calls the "collectstatic" django command
collect:
	$(MANAGE) collectstatic --settings=$(SETTINGS) --noinput

# target: migrate - run migrations.
migrate:
	$(MANAGE) migrate --settings=$(SETTINGS) --noinput

# target: rebuild - clean, update, collect, then FLUSH all data. WARNING: this command will flush your database.
rebuild: clean update collect
	$(MANAGE) flush --settings=$(SETTINGS) --noinput

# target: run - run the project
run:
	$(MANAGE) runserver --settings=$(SETTINGS)

# target: deploy - deploy project to heroku
deploy:
	git push heroku master
	heroku run $(MANAGE) migrate --noinput

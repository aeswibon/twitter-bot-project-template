.DEFAULT_GOAL := help

.PHONY: help
help:			## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: install
install:		## Install the dependencies
	@echo "Installing the dependencies"
	@pipenv install --categories "packages dev-packages"
	@pipenv run pre-commit install

.PHONY: run
run:			## Run the application locally
	@echo "Running the application"
	@pipenv run python manage.py runserver 9000

.PHONY: migrations
migrations:		## Create migrations locally
	@echo "Creating migrations"
	@pipenv run python manage.py makemigrations

.PHONY: migrate
migrate:		## Apply migrations locally
	@echo "Applying migrations"
	@pipenv run python manage.py migrate


.PHONY: format
format:			## Format the code
	@echo "Formatting the code"
	@pipenv run pre-commit run --all-files

.PHONY: shell
shell:			## Run the shell locally
	@echo "Running the shell"
	@pipenv run python manage.py shell


.PHONY: build
build:			## Build the application with docker
	@echo "Building the application with docker"
	@docker compose build

.PHONY: up
up:			## Start the application with docker
	@echo "Starting the application with docker"
	@docker compose up -d

.PHONY: down
down:			## Stop the application on docker
	@echo "Stopping the application with docker"
	@docker compose down

.PHONY: logs
logs:			## Show the logs of the application on docker
	@echo "Showing the logs"
	@docker compose logs --follow

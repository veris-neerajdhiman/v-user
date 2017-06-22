
.PHONY: runserver
runserver:
	python manage.py runserver 0.0.0.0:8013

.PHONY: migrations
migrations:
	python manage.py makemigrations

.PHONY: migrate
migration:
	python manage.py migrate

.PHONY: db_shell
db_shell:
	python manage.py dbshell

.PHONY: shell
shell:
	python manage.py shell_plus

.PHONY: superuser
superuser:
	python manage.py createsuperuser

.PHONY: test
test:
	python manage.py test

# ---------------------------------------------------------------------------------------------------

# Makefile commands for docker


# -----------------------------------------------------------------------------------------------------

# Docker commands

.PHONY: build
build:
	docker build -t inforian/user-service:${version} -f config/docker/Dockerfile .

.PHONY: image
image:
	docker images | grep user-service

.PHONY: tag
tag:
	docker tag ${id} inforian/user-service:${version}

.PHONY: push
push:
	docker push inforian/user-service:${version}

.PHONY: run
run:
	docker run -it --publish=8001:8000 $(id)

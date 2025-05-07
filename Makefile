dev:
	uv run python manage.py runserver

install:
	uv sync

collectstatic:
	uv run django-admin collectstatic

migrate:
	uv run python manage.py makemigrations
	uv run python manage.py migrate

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi
build:
	sudo docker-compose up --no-start --remove-orphans --build

start:
	docker-compose start

stop:
	docker-compose stop

up:
	docker-compose up

test: start
	docker-compose exec django-backend python3 /app/manage.py test
	make stop

migrate: start
	docker-compose exec django-backend python3 /app/manage.py migrate

run: migrate
	docker-compose logs -f


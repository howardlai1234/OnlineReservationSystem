migrate-db:
	docker-compose run --rm ors python3 manage.py migrate

add-super-user:
	docker-compose run --rm ors python3 manage.py createsuperuser

create-migration:
	docker-compose run --rm ors python3 manage.py makemigrations
	
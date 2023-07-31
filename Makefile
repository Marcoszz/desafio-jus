create-conn:
	docker network create conn

start:
	docker compose up selenium web

tests:
	docker exec desafio-jus-web-1 python -m pytest tests/ -v -W ignore::DeprecationWarning



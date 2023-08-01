build:
	docker network create conn

up:
	docker compose up selenium web --build

test:
	docker exec desafio-jus-web-1 python -m pytest ../tests/ -v -W ignore::DeprecationWarning



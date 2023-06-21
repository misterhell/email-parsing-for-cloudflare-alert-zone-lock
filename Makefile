


project_init:
	mkdir tmp
	touch tmp/app.log


start:
	docker compose up -d

stop:
	docker compose stop

status:
	docker compose ps
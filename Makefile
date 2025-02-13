build:
	docker-compose --env-file srcs/.env -f srcs/docker-compose.yml up --build

prod:
	docker-compose --env-file srcs/.prod.env -f srcs/docker-compose.prod.yml up --build

up:
	docker-compose --env-file srcs/.env -f srcs/docker-compose.yml up

prud:
	docker-compose --env-file srcs/.prod.env -f srcs/docker-compose.prod.yml up

stop:
	docker-compose --env-file srcs/.env -f srcs/docker-compose.yml stop

pstop:
	docker-compose --env-file srcs/.prod.env -f srcs/docker-compose.prod.yml stop

down:
	docker-compose -f srcs/docker-compose.yml down --remove-orphans -v --rmi all

pdown:
	docker-compose -f srcs/docker-compose.prod.yml down --remove-orphans -v --rmi all

ps:
	docker-compose -f srcs/docker-compose.yml ps

pps:
	docker-compose -f srcs/docker-compose.prod.yml ps

logs:
	docker-compose -f srcs/docker-compose.yml logs

plogs:
	docker-compose -f srcs/docker-compose.prod.yml logs

prune:
	docker system prune -af

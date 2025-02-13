
 ________  ___  ___  _______   ________  _________        ________  ___  ___  _______   _______  _________   
|\   ____\|\  \|\  \|\  ___ \ |\   __  \|\___   ___\     |\   ____\|\  \|\  \|\  ___ \ |\  ___ \|\___   ___\ 
\ \  \___|\ \  \\\  \ \   __/|\ \  \|\  \|___ \  \_|     \ \  \___|\ \  \\\  \ \   __/|\ \   __/\|___ \  \_| 
 \ \  \    \ \   __  \ \  \_|/_\ \   __  \   \ \  \       \ \_____  \ \   __  \ \  \_|/_\ \  \_|/__  \ \  \  
  \ \  \____\ \  \ \  \ \  \_|\ \ \  \ \  \   \ \  \       \|____|\  \ \  \ \  \ \  \_|\ \ \  \_|\ \  \ \  \ 
   \ \_______\ \__\ \__\ \_______\ \__\ \__\   \ \__\        ____\_\  \ \__\ \__\ \_______\ \_______\  \ \__\
    \|_______|\|__|\|__|\|_______|\|__|\|__|    \|__|       |\_________\|__|\|__|\|_______|\|_______|   \|__|
                                                            \|_________|                                     
                                                                                                             
                                                                                                             
Makefile cmds:
    -make (ou make build): build for dev
    -make prod: build for prod
    -make up / prud: docker-compose up dev / prod
    -make stop / pstop
    -make down / pdown
    -make ps / pps
    -make logs / plogs
    -make prune

Connect:
	http://<IP>:8000 -> dev
	https://<IP>:4443 -> prod

Debug dockers:

    sudo docker exec -it <container_name> bash -> naviguer dans les fichiers du container
    (si django admin en panne): psql --username=<username> --dbname=<dbname>
        psql cheat sheet: https://medium.com/@neeswebservice/postgresql-cheatsheet-all-in-one-823c73fdcc95

lil tips:

    Utilisez Docker Desktop si vous etes sur mac pour avoir les daemons.
    Un simple make down/pdown suffit a supprimer tous les containers/volumes/images.
    Je ne recharge pas constamment le static_volume donc il faut remake apres chaque modif.


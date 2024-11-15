necessite :
- dbeaver pour les connections postgrSQL

structure basique du projet :
.env
doit contenir impérativement les elements suivants :
# MinIO 
MINIO_ACCESS_KEY= 
MINIO_SECRET_KEY= 

# Postgres
POSTGRES_ACCESS_KEY= 
POSTGRES_ACCESS_KEY= 
_______________________________________________________________
docker-compose.yaml
Dockerfile
Makefile

_______________________________________________________________

dans metabase pour la connection postgresql il faut rentrer host.docker.internal pour le nom d'hote.

une fois tout en place il faut simplement faire un make build(le build est un peu long dus a driver pour selenium)
, puis un make up 
pour le makefile il faut d'abord installer MinGW et l'ajouter au PATH 


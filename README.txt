__________________________________________________________________________________________________________________________
Stack de Données Moderne et open source.
combine plusieurs outils de l'extraction des données a l'analyse avec stockage objet et bdd relationelle ainsi qu'un vector store pour l'integration 
dans des applications d'IA et de ML.
_________________________________________________________________________________________________________________________

Architecture :

- MAGE
 pour la partie ETL et l'orchestration des pipelines.
 (les dépendances pour Selenium dont intégrés dans le dockerfile pour le scrapping)

- MinIo
 pour le stockage objet 

- PostgreSQL
 base de données relationelle connectable a metabase pour la partie analyse de données

- Qdrant 
 vector store pour les recherches par similarités et le stockage de vecteurs pour les applications IA

- Metabase 
 partie Business Intelligence

_________________________________________________________________________________________________________________________

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
_________________________________________________________________________________________________________________________
dans metabase pour la connection postgresql il faut rentrer host.docker.internal pour le nom d'hote.

une fois tout en place il faut simplement faire un make build (le build est un peu long dus a driver pour selenium)
, puis un make up 
pour le makefile il faut d'abord installer MinGW et l'ajouter au PATH 



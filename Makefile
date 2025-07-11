IMAGE_NAME = mage_demo

COMPOSE_FILE = docker-compose.yaml

build:
	docker build -t $(IMAGE_NAME) .

up:
	docker-compose -f $(COMPOSE_FILE) up -d

down:
	docker-compose -f $(COMPOSE_FILE) down

browse:
	open http://localhost:6789

create:
	docker run -it -p 6789:6789 -v $(PWD):/home/src mageai/mageai \
  /app/run_app.sh mage start $(IMAGE_NAME)

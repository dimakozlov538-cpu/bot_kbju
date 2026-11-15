IMAGE_NAME = my_telegram_bot
CONTAINER_NAME = my_bot_container

help:
	@echo "Доступные команды:"
	@echo "  make build   - Собрать Docker-образ"
	@echo "  make run     - Запустить бота в фоне"
	@echo "  make stop    - Остановить и удалить контейнер"
	@echo "  make restart - Пересобрать и перезапустить бота (после правок в коде)"
	@echo "  make logs    - Посмотреть логи работы бота"

build:
	docker build --pull=false -t $(IMAGE_NAME) .

run:
	docker run -d --name $(CONTAINER_NAME) --restart unless-stopped --env-file .env $(IMAGE_NAME)

stop:
	-docker stop $(CONTAINER_NAME)
	-docker rm $(CONTAINER_NAME)

restart: stop build run

logs:
	docker logs -f $(CONTAINER_NAME)

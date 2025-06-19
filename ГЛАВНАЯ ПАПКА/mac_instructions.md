## Установка зависимостей
pip install -r requirements.txt

## Запуск Kafka и Kafka UI
docker-compose up -d

http://localhost:8082

## Компиляция Proto-файлов
cd social_network/proto
python compile.py
cd ../..

### Терминал 1 - gRPC сервер:
python -m social_network.core.server

### Терминал 2 - REST API:
python -m social_network.api.rest_api

## Запуск тестов
python -m social_network.tests.test_api

## Генерация тестовых сообщений в Kafka
python -m social_network.tools.generate_kafka_messages --count 20 --interval 0.5

## Структура проекта

- `social_network/api/rest_api.py` - REST API (первый сервис)
- `social_network/core/server.py` - gRPC сервер (второй сервис)
- `social_network/proto/service.proto` - Определение gRPC сервиса
- `social_network/tests/test_api.py` - Тесты для API
- `social_network/tools/generate_kafka_messages.py` - Скрипт для генерации тестовых сообщений
- `docker-compose.yml` - Конфигурация Docker Compose для Kafka и Zookeeper


### Социальная сеть
- `POST /register` - Регистрация клиента
- `POST /get_post` - Получение поста
- `POST /create_comment` - Создание комментария к посту
- `GET /get_comments` - Получение комментариев к посту с пагинацией

### Платформа программ лояльности
- `POST /get_promocode` - Получение промокода
- `POST /click_promocode` - Клик по промокоду
- `POST /create_promocode_comment` - Создание комментария к промокоду
- `GET /get_promocode_comments` - Получение комментариев к промокоду с пагинацией

### Регистрация клиента
```bash
curl -X POST http://localhost:5001/register \
  -H "Content-Type: application/json" \
  -d '{"client_id": "user123"}'
```

### Получение поста
```bash
curl -X POST http://localhost:5001/get_post \
  -H "Content-Type: application/json" \
  -d '{"client_id": "user123", "post_id": "post456"}'
```

### Создание комментария к посту
```bash
curl -X POST http://localhost:5001/create_comment \
  -H "Content-Type: application/json" \
  -d '{"client_id": "user123", "post_id": "post456", "comment_text": "Отличный пост!"}'
```

### Получение комментариев к посту
```bash
curl -X GET "http://localhost:5001/get_comments?post_id=post456&page=1&page_size=10"
```

### Получение промокода
```bash
curl -X POST http://localhost:5001/get_promocode \
  -H "Content-Type: application/json" \
  -d '{"client_id": "user123", "promocode_id": "promo789"}'
```

### Клик по промокоду
```bash
curl -X POST http://localhost:5001/click_promocode \
  -H "Content-Type: application/json" \
  -d '{"client_id": "user123", "promocode_id": "promo789"}'
```

### Создание комментария к промокоду
```bash
curl -X POST http://localhost:5001/create_promocode_comment \
  -H "Content-Type: application/json" \
  -d '{"client_id": "user123", "promocode_id": "promo789", "comment_text": "Отличный промокод!"}'
```

### Получение комментариев к промокоду
```bash
curl -X GET "http://localhost:5001/get_promocode_comments?promocode_id=promo789&page=1&page_size=10"
```
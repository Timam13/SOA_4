"""
Скрипт для автоматической настройки Kafka UI через API.
"""

import requests
import time
import json
import logging
import sys

# логи
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KAFKA_UI_URL = "http://localhost:8082/api"

def wait_for_kafka_ui(max_retries=30, retry_interval=1):
    logger.info(f"Ожидание запуска Kafka UI на {KAFKA_UI_URL}...")
    
    for i in range(max_retries):
        try:
            response = requests.get(f"{KAFKA_UI_URL}/clusters", timeout=2)
            if response.status_code == 200:
                logger.info("Kafka UI доступен")
                return True
        except requests.exceptions.RequestException:
            pass
        
        logger.info(f"Попытка {i+1}/{max_retries}...")
        time.sleep(retry_interval)
    
    logger.error(f"Kafka UI не запустился за {max_retries * retry_interval} секунд")
    return False

def configure_kafka_cluster():
    logger.info("Настройка кластера Kafka в Kafka UI...")
    
    # Проверяем, существует ли уже кластер с таким именем
    try:
        response = requests.get(f"{KAFKA_UI_URL}/clusters", timeout=5)
        if response.status_code == 200:
            clusters = response.json()
            for cluster in clusters:
                if cluster.get("name") == "Social Network Kafka":
                    logger.info("Кластер 'Social Network Kafka' уже существует")
                    return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при проверке существующих кластеров: {e}")
        return False
    
    # Создаем новый кластер
    cluster_config = {
        "name": "Social Network Kafka",
        "bootstrapServers": "PLAINTEXT://kafka:29092",
        "properties": {},
        "readOnly": False,
        "jmxConfig": {
            "scheme": "http",
            "host": "kafka",
            "port": 9997
        }
    }
    
    try:
        response = requests.post(
            f"{KAFKA_UI_URL}/clusters", 
            json=cluster_config,
            timeout=5
        )
        
        if response.status_code in [200, 201, 204]:
            logger.info("Кластер 'Social Network Kafka' успешно создан")
            return True
        else:
            logger.error(f"Ошибка при создании кластера: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при создании кластера: {e}")
        return False

def main():
    # Ждем запуска Kafka UI
    if not wait_for_kafka_ui():
        sys.exit(1)
    
    if configure_kafka_cluster():
        logger.info("Настройка Kafka UI завершена успешно")
        sys.exit(0)
    else:
        logger.error("Не удалось настроить Kafka UI")
        sys.exit(1)

if __name__ == "__main__":
    main()
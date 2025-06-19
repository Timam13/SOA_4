import os
import json
import logging

# логи
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

servers = BOOTSTRAP.split(",")

producer = None
try:
    from kafka import KafkaProducer
    producer = KafkaProducer(
        bootstrap_servers=servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    logger.info(f"Kafka подключена: {BOOTSTRAP}")
except Exception as e:
    logger.warning(f"Не удалось подключиться к Kafka: {e}")
    logger.warning("Будет использована заглушка вместо Kafka")

def send(topic, message):
    if producer:
        try:
            producer.send(topic, message)
            producer.flush()
            logger.info(f"[Kafka] {topic}: {message}")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения в Kafka: {e}")
    else:
        # Заглушка для случая, когда Kafka недоступна
        logger.info(f"[Заглушка] {topic}: {message}")

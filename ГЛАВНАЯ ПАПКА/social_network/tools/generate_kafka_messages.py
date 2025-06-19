"""
Скрипт для генерации тестовых сообщений в Kafka.
Полезно для демонстрации работы Kafka UI.
"""

import os
import sys
import json
import time
import random
import datetime
import logging

# Добавляем родительскую директорию в sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from core.kafka_producer import send

# логи
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Тестовые данные
client_ids = ["user1", "user2", "user3", "user4", "user5"]
post_ids = ["post1", "post2", "post3", "post4", "post5"]
promocode_ids = ["promo1", "promo2", "promo3", "promo4", "promo5"]
comments = [
    "Отличный пост!",
    "Интересная информация",
    "Спасибо за пост",
    "Не согласен с автором",
    "Хотелось бы больше деталей",
    "Очень полезно",
    "Первый комментарий!",
    "Лайк и подписка",
    "Жду продолжения",
    "Супер!"
]
promocode_comments = [
    "Отличный промокод!",
    "Скидка работает",
    "Спасибо за промокод",
    "Не работает",
    "Срок действия истек",
    "Очень выгодно",
    "Первый раз использую",
    "Буду использовать еще",
    "Рекомендую всем",
    "Класс!"
]

def generate_view_message():
    client_id = random.choice(client_ids)
    post_id = random.choice(post_ids)
    
    message = {
        "client_id": client_id,
        "post_id": post_id,
        "action": "view",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    
    send("post_views", message)
    logger.info(f"Отправлено сообщение о просмотре: {message}")



def generate_comment_message():
    client_id = random.choice(client_ids)
    post_id = random.choice(post_ids)
    comment_text = random.choice(comments)
    
    message = {
        "client_id": client_id,
        "post_id": post_id,
        "action": "comment",
        "comment_text": comment_text,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    
    send("post_comments", message)
    logger.info(f"Отправлено сообщение о комментарии: {message}")

def generate_registration_message():
    client_id = f"new_user_{random.randint(100, 999)}"
    
    message = {
        "client_id": client_id,
        "registration_date": datetime.datetime.utcnow().isoformat()
    }
    
    send("client_registration", message)
    logger.info(f"Отправлено сообщение о регистрации: {message}")

def generate_promocode_view_message():
    client_id = random.choice(client_ids)
    promocode_id = random.choice(promocode_ids)
    
    message = {
        "client_id": client_id,
        "promocode_id": promocode_id,
        "action": "view",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    
    send("promocode_views", message)
    logger.info(f"Отправлено сообщение о просмотре промокода: {message}")

def generate_promocode_click_message():
    client_id = random.choice(client_ids)
    promocode_id = random.choice(promocode_ids)
    
    message = {
        "client_id": client_id,
        "promocode_id": promocode_id,
        "action": "click",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    
    send("promocode_clicks", message)
    logger.info(f"Отправлено сообщение о клике по промокоду: {message}")

def generate_promocode_comment_message():
    client_id = random.choice(client_ids)
    promocode_id = random.choice(promocode_ids)
    comment_text = random.choice(promocode_comments)
    
    message = {
        "client_id": client_id,
        "promocode_id": promocode_id,
        "action": "comment",
        "comment_text": comment_text,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    
    send("promocode_comments", message)
    logger.info(f"Отправлено сообщение о комментарии к промокоду: {message}")

def generate_random_messages(count=10, interval=1):
    
    logger.info(f"Генерация {count} случайных сообщений с интервалом {interval} сек...")
    
    for i in range(count):
        # Выбираем случайный тип сообщения
        message_type = random.choice([
            "view", "comment", "registration",
            "promocode_view", "promocode_click", "promocode_comment"
        ])
        
        if message_type == "view":
            generate_view_message()
        elif message_type == "comment":
            generate_comment_message()
        elif message_type == "registration":
            generate_registration_message()
        elif message_type == "promocode_view":
            generate_promocode_view_message()
        elif message_type == "promocode_click":
            generate_promocode_click_message()
        elif message_type == "promocode_comment":
            generate_promocode_comment_message()
        
        # Пауза между сообщениями
        if i < count - 1:
            time.sleep(interval)
    
    logger.info(f"Сгенерировано {count} сообщений")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Генерация тестовых сообщений в Kafka")
    parser.add_argument("--count", type=int, default=10, help="Количество сообщений")
    parser.add_argument("--interval", type=float, default=1.0, help="Интервал между сообщениями в секундах")
    
    args = parser.parse_args()
    
    generate_random_messages(args.count, args.interval)
import requests
import time
import sys
import logging
import os

# логи
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("api_tests")

BASE_URL = "http://localhost:5001"

def wait_for_services(max_retries=5, retry_interval=1):
    logger.info("Проверка доступности сервисов...")
    
    for i in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/", timeout=1)
            if response.status_code == 200:
                logger.info("REST API сервер доступен")
                return True
        except requests.exceptions.RequestException:
            logger.info(f"Ожидание запуска сервисов... Попытка {i+1}/{max_retries}")
            time.sleep(retry_interval)
    
    logger.error("Сервисы не запустились за отведенное время")
    return False

def test_register_client():
    logger.info("Тест регистрации клиента...")
    try:
        response = requests.post(
            f"{BASE_URL}/register",
            json={"client_id": "test_user_1"},
            timeout=5
        )
        logger.info(f"Статус: {response.status_code}")
        logger.info(f"Ответ: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Ошибка при тестировании регистрации клиента: {e}")
        return False

def test_get_post():
    logger.info("Тест получения поста...")
    try:
        response = requests.post(
            f"{BASE_URL}/get_post",
            json={"client_id": "test_user_1", "post_id": "test_post_1"},
            timeout=5
        )
        logger.info(f"Статус: {response.status_code}")
        logger.info(f"Ответ: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Ошибка при тестировании получения поста: {e}")
        return False



def test_create_comment():
    logger.info("Тест создания комментария...")
    try:
        response = requests.post(
            f"{BASE_URL}/create_comment",
            json={
                "client_id": "test_user_1", 
                "post_id": "test_post_1",
                "comment_text": "Это тестовый комментарий"
            },
            timeout=5
        )
        logger.info(f"Статус: {response.status_code}")
        logger.info(f"Ответ: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Ошибка при тестировании создания комментария: {e}")
        return False

def test_get_comments():
    logger.info("Тест получения комментариев к посту...")
    try:
        # Create
        requests.post(
            f"{BASE_URL}/create_comment",
            json={
                "client_id": "test_user_1", 
                "post_id": "test_post_1",
                "comment_text": "Это тестовый комментарий для проверки пагинации"
            },
            timeout=5
        )
        
        # Get
        response = requests.get(
            f"{BASE_URL}/get_comments?post_id=test_post_1&page=1&page_size=10",
            timeout=5
        )
        logger.info(f"Статус: {response.status_code}")
        logger.info(f"Ответ: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Ошибка при тестировании получения комментариев: {e}")
        return False

def test_get_promocode():
    logger.info("Тест получения промокода...")
    try:
        response = requests.post(
            f"{BASE_URL}/get_promocode",
            json={"client_id": "test_user_1", "promocode_id": "test_promo_1"},
            timeout=5
        )
        logger.info(f"Статус: {response.status_code}")
        logger.info(f"Ответ: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Ошибка при тестировании получения промокода: {e}")
        return False

def test_click_promocode():
    logger.info("Тест клика по промокоду...")
    try:
        response = requests.post(
            f"{BASE_URL}/click_promocode",
            json={"client_id": "test_user_1", "promocode_id": "test_promo_1"},
            timeout=5
        )
        logger.info(f"Статус: {response.status_code}")
        logger.info(f"Ответ: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Ошибка при тестировании клика по промокоду: {e}")
        return False

def test_create_promocode_comment():
    logger.info("Тест создания комментария к промокоду...")
    try:
        response = requests.post(
            f"{BASE_URL}/create_promocode_comment",
            json={
                "client_id": "test_user_1", 
                "promocode_id": "test_promo_1",
                "comment_text": "Это тестовый комментарий к промокоду"
            },
            timeout=5
        )
        logger.info(f"Статус: {response.status_code}")
        logger.info(f"Ответ: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Ошибка при тестировании создания комментария к промокоду: {e}")
        return False

def test_get_promocode_comments():
    logger.info("Тест получения комментариев к промокоду...")
    try:
        # Create комментарий
        requests.post(
            f"{BASE_URL}/create_promocode_comment",
            json={
                "client_id": "test_user_1", 
                "promocode_id": "test_promo_1",
                "comment_text": "Это тестовый комментарий к промокоду для проверки пагинации"
            },
            timeout=5
        )
        
        # Get комментарии
        response = requests.get(
            f"{BASE_URL}/get_promocode_comments?promocode_id=test_promo_1&page=1&page_size=10",
            timeout=5
        )
        logger.info(f"Статус: {response.status_code}")
        logger.info(f"Ответ: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Ошибка при тестировании получения комментариев к промокоду: {e}")
        return False

def run_all_tests():
    """Запуск всех тестов API"""
    logger.info("=" * 50)
    logger.info("Запуск тестов API...")
    logger.info("=" * 50)
    
    if not wait_for_services():
        return 1
 
    tests = [
        test_register_client,
        test_get_post,
        test_create_comment,
        test_get_comments,
        test_get_promocode,
        test_click_promocode,
        test_create_promocode_comment,
        test_get_promocode_comments
    ]
    
    # cal complete tests
    success = 0
    for test in tests:
        if test():
            success += 1
    
    # res
    logger.info("=" * 50)
    logger.info(f"Результаты: {success}/{len(tests)} тестов успешно")
    
    if success == len(tests):
        logger.info("Все тесты пройдены успешно!")
        return 0
    else:
        logger.error("Некоторые тесты не пройдены.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())

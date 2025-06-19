"""
CLI для управления сервисами социальной сети.
"""

import argparse
import subprocess
import sys
import time
import os
import signal

# Проверяем, сгенерированы ли proto-файлы
try:
    # Добавляем путь к директории с proto-файлами в sys.path
    proto_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'social_network', 'proto')
    if proto_dir not in sys.path:
        sys.path.append(proto_dir)
    
    import service_pb2
    import service_pb2_grpc
except ImportError:
    print("ОШИБКА: Proto-файлы не сгенерированы или не найдены!")
    print("Запустите: helper.bat для Windows")
    sys.exit(1)

# Список запущенных процессов
processes = []

def _start_process(cmd):
    """Запускает процесс и добавляет его в список процессов"""
    process = subprocess.Popen(cmd, env=os.environ)
    processes.append(process)
    return process

def start():
    print("Запуск gRPC сервера...")
    _start_process([sys.executable, "-m", "social_network.core.server"])
    
    time.sleep(1)
    
    print("Запуск REST API...")
    _start_process([sys.executable, "-m", "social_network.api.rest_api"])
    
    print("Все сервисы запущены. Нажмите Ctrl+C для остановки.")
    
    try:
        for process in processes:
            process.wait()
    except KeyboardInterrupt:
        stop()

def stop():
    print("\nОстановка всех сервисов...")
    for process in processes:
        if process.poll() is None:
            process.terminate()
    sys.exit(0)

def test():
    print("Запуск тестов...")
    
    grpc_process = subprocess.Popen([sys.executable, "-m", "social_network.core.server"])
    
    time.sleep(1)
    
    api_process = subprocess.Popen([sys.executable, "-m", "social_network.api.rest_api"])

    time.sleep(1)
    
    test_result = subprocess.call([sys.executable, "-m", "social_network.tests.test_api"])
    
    grpc_process.terminate()
    api_process.terminate()

    sys.exit(test_result)

def main():
    parser = argparse.ArgumentParser(description="Управление сервисами социальной сети")
    parser.add_argument("command", choices=["start", "stop", "test"], 
                        help="Команда для выполнения")
    
    args = parser.parse_args()
    
    if args.command == "start":
        start()
    elif args.command == "stop":
        stop()
    elif args.command == "test":
        test()

if __name__ == "__main__":
    main()

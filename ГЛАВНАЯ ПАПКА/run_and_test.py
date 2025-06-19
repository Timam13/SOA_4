import subprocess
import time
import sys
import os

def main():
    print("Запуск gRPC сервера...")
    grpc_server = subprocess.Popen(
        [sys.executable, "-m", "social_network.core.server"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(2)
    
    print("Запуск REST API...")
    rest_api = subprocess.Popen(
        [sys.executable, "-m", "social_network.api.rest_api"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    time.sleep(2)
    
    print("Запуск тестов...")
    test_result = subprocess.run(
        [sys.executable, "-m", "social_network.tests.test_api"],
        capture_output=True,
        text=True
    )
    
    print(test_result.stdout)
    print(test_result.stderr)
    
    print("Остановка сервисов...")
    grpc_server.terminate()
    rest_api.terminate()
    
    return test_result.returncode

if __name__ == "__main__":
    sys.exit(main())

# Пакет proto
import os
import sys

# Добавляем текущую директорию в sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    # Импортируем сгенерированные файлы
    from service_pb2 import *
    from service_pb2_grpc import *
except ImportError:
    # Файлы еще не сгенерированы
    pass

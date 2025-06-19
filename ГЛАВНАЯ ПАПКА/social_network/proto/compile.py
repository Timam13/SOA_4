"""
Скрипт для компиляции proto-файлов.
"""

import os
import subprocess
import sys

def compile_proto():
    proto_dir = os.path.dirname(os.path.abspath(__file__))
    
    cmd = [
        sys.executable, "-m", "grpc_tools.protoc",
        f"-I{proto_dir}",
        f"--python_out={proto_dir}",
        f"--grpc_python_out={proto_dir}",
        os.path.join(proto_dir, "service.proto")
    ]
    
    print(f"Выполняем команду: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=True)
    
    if result.returncode == 0:
        print("Proto-файлы успешно скомпилированы")
    else:
        print("Ошибка при компиляции proto-файлов")
        sys.exit(1)

if __name__ == "__main__":
    compile_proto()

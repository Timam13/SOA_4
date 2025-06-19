from setuptools import setup, find_packages

setup(
    name="social_network_simple",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask", 
        "grpcio", 
        "grpcio-tools", 
        "protobuf",
        "kafka-python", 
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "social-network=social_network.cli:main"
        ]
    }
)
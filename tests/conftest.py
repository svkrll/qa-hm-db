import pytest
import pymysql
from pymysql.cursors import DictCursor
import random
import string
from datetime import datetime

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.db import (
    create_customer,
    delete_customer_by_id
)

def pytest_addoption(parser):
    parser.addoption("--host", action="store", default="localhost", help="DB host")
    parser.addoption("--port", action="store", default="3306", help="DB port")
    parser.addoption("--user", action="store", default="root", help="DB user")
    parser.addoption("--password", action="store", default="", help="DB password")
    parser.addoption("--database", action="store", default="opencart", help="DB name")

@pytest.fixture(scope="session")
def connection(request):
    host = request.config.getoption("--host")
    port = int(request.config.getoption("--port"))
    user = request.config.getoption("--user")
    password = request.config.getoption("--password")
    database = request.config.getoption("--database")

    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        cursorclass=DictCursor,
        autocommit=False
    )
    yield conn
    conn.close()

def generate_random_string(length=6):
    return ''.join(random.choices(string.ascii_letters, k=length))

def generate_random_email():
    return f"{generate_random_string()}@example.com"

def generate_random_phone():
    return f"+79{random.randint(100000000, 999999999)}"

@pytest.fixture
def raw_customer_data():
    """
    Возвращает словарь с рандомизированными полями для нового клиента.
    """
    return {
        "customer_group_id": 1,
        "store_id": 0,
        "language_id": 1,
        "firstname": "Test",
        "lastname": "User",
        "email": generate_random_email(),
        "telephone": generate_random_phone(),
        "password": "hashed_pass",      # предполагаем, что хэширование уже выполнено
        "custom_field": "{}",           # JSON-строка, если не используется — можно оставить пустой объект
        "newsletter": 0,
        "ip": "192.168.0.2",
        "status": 1,
        "safe": 1,
        "token": "AAAAABBBBBCCCCDDDD",
        "code": "123123",
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@pytest.fixture
def created_customer(connection, raw_customer_data):
    """
    Создаёт клиента в БД перед тестом и удаляет его после.
    Возвращает ID созданного клиента.
    """
    customer_id = create_customer(connection, raw_customer_data)
    yield customer_id
    # В teardown-фазе обязательно пытаемся удалить клиента.
    # Если в самом тесте клиент уже был удалён, delete_customer_by_id должен вернуть 0 и ничего страшного не произойдет.
    delete_customer_by_id(connection, customer_id)

import pytest
import allure
import random
import string
from lib.db import (
    create_customer,
    get_customer_by_id,
    update_customer_status,
    delete_customer_by_id,
    get_customer_by_email,
)

def generate_random_string(length=6):
    return ''.join(random.choices(string.ascii_letters, k=length))

def generate_random_email():
    return f"{generate_random_string()}@example.com"

def generate_random_phone():
    return f"+79{random.randint(100000000, 999999999)}"

@pytest.fixture
def test_customer_data():
    return {
        "firstname": "Test",
        "lastname": "User",
        "email": generate_random_email(),
        "telephone": generate_random_phone(),
        "password": "hashed_pass",  # Предполагем, что пароль уже хэширован
        "newsletter": 0,
        "status": 1,
    }

@allure.feature("Клиенты")
@allure.story("Создание клиента")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_customer_and_verify_by_id(connection, test_customer_data):
    with allure.step("Создание клиента"):
        customer_id = create_customer(connection, test_customer_data)

    with allure.step("Проверка клиента по ID"):
        customer = get_customer_by_id(connection, customer_id)
        assert customer is not None
        assert customer["email"] == test_customer_data["email"]
        assert customer["firstname"] == test_customer_data["firstname"]


@allure.feature("Клиенты")
@allure.story("Обновление клиента")
@allure.severity(allure.severity_level.NORMAL)
def test_update_existing_customer(connection, test_customer_data):
    with allure.step("Создание клиента"):
        customer_id = create_customer(connection, test_customer_data)

    updated_data = {
        "firstname": "Updated",
        "lastname": "User",
        "email": generate_random_email(),
        "telephone": "9999999999",
    }

    with allure.step("Обновление данных клиента"):
        query = """
            UPDATE oc_customer
            SET firstname = %s, lastname = %s, email = %s, telephone = %s
            WHERE customer_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, (
                updated_data["firstname"],
                updated_data["lastname"],
                updated_data["email"],
                updated_data["telephone"],
                customer_id
            ))
            connection.commit()

    with allure.step("Проверка обновлённых данных"):
        customer = get_customer_by_id(connection, customer_id)
        assert customer["firstname"] == updated_data["firstname"]
        assert customer["lastname"] == updated_data["lastname"]
        assert customer["email"] == updated_data["email"]
        assert customer["telephone"] == updated_data["telephone"]


@allure.feature("Клиенты")
@allure.story("Негативное обновление несуществующего клиента")
@allure.severity(allure.severity_level.MINOR)
def test_update_nonexistent_customer(connection):
    fake_id = 999999
    updated_data = ("Ghost", "User", "ghost@example.com", "0000000000", fake_id)

    with allure.step("Попытка обновить клиента с несуществующим ID"):
        query = """
            UPDATE oc_customer
            SET firstname = %s, lastname = %s, email = %s, telephone = %s
            WHERE customer_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, updated_data)
            connection.commit()
            assert cursor.rowcount == 0


@allure.feature("Клиенты")
@allure.story("Удаление клиента")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_existing_customer(connection, test_customer_data):
    with allure.step("Создание клиента"):
        customer_id = create_customer(connection, test_customer_data)

    with allure.step("Удаление клиента"):
        deleted = delete_customer_by_id(connection, customer_id)
        assert deleted == 1

    with allure.step("Проверка отсутствия клиента"):
        customer = get_customer_by_id(connection, customer_id)
        assert customer is None


@allure.feature("Клиенты")
@allure.story("Негативное удаление несуществующего клиента")
@allure.severity(allure.severity_level.MINOR)
def test_delete_nonexistent_customer(connection):
    fake_id = 999999
    with allure.step("Попытка удалить несуществующего клиента"):
        deleted = delete_customer_by_id(connection, fake_id)
        assert deleted == 0

##### Дополнительные тесты #####
@allure.feature("Клиенты")
@allure.story("Поиск клиента по email")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_customer_by_email(connection, test_customer_data):
    with allure.step("Создание клиента"):
        customer_id = create_customer(connection, test_customer_data)

    with allure.step("Поиск клиента по email"):
        customer = get_customer_by_email(connection, test_customer_data["email"])
        assert customer is not None
        assert customer["customer_id"] == customer_id
        assert customer["email"] == test_customer_data["email"]
        assert customer["firstname"] == test_customer_data["firstname"]

@allure.feature("Клиенты")
@allure.story("Поиск клиента по несуществующему email")
@allure.severity(allure.severity_level.NORMAL)
def test_get_nonexistent_customer_by_email(connection):
    fake_email = f"nonexistent_{generate_random_string()}@example.com"

    with allure.step("Попытка найти клиента по несуществующему email"):
        customer = get_customer_by_email(connection, fake_email)
        assert customer is None

@allure.feature("Клиенты")
@allure.story("Обновление статуса клиента")
@allure.severity(allure.severity_level.NORMAL)
def test_update_customer_status_existing(connection, test_customer_data):
    with allure.step("Создание клиента"):
        customer_id = create_customer(connection, test_customer_data)

    with allure.step("Изменение статуса клиента на 0 (неактивен)"):
        update_customer_status(connection, customer_id, 0)

    with allure.step("Проверка обновлённого статуса клиента"):
        customer = get_customer_by_id(connection, customer_id)
        assert customer is not None
        assert customer["status"] == 0

@allure.feature("Клиенты")
@allure.story("Обновление статуса несуществующего клиента")
@allure.severity(allure.severity_level.MINOR)
def test_update_customer_status_nonexistent(connection):
    fake_id = 999999

    with allure.step("Попытка обновить статус несуществующего клиента"):
        update_customer_status(connection, fake_id, 0)

    with allure.step("Проверка, что клиент не появился в базе"):
        customer = get_customer_by_id(connection, fake_id)
        assert customer is None


import pytest
import allure
from lib.db import (
    create_customer,
    get_customer_by_id,
    update_customer_status,
    delete_customer_by_id,
    get_customer_by_email,
    update_customer
)

from conftest import generate_random_string, generate_random_email 

@allure.feature("Клиенты")
@allure.story("Создание клиента")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_customer_and_verify_by_id(connection, raw_customer_data):
    """
    Здесь проверяем логику создания клиента:
    1) создаём руками в теле теста на основе raw_customer_data,
    2) убеждаемся, что get_customer_by_id возвращает правильные поля,
    3) затем явно удаляем клиента в блоке finally.
    """
    customer_id = create_customer(connection, raw_customer_data)
    try:
        customer = get_customer_by_id(connection, customer_id)
        assert customer is not None
        assert customer["email"] == raw_customer_data["email"]
        assert customer["firstname"] == raw_customer_data["firstname"]
    finally:
        delete_customer_by_id(connection, customer_id)

@allure.feature("Клиенты")
@allure.story("Обновление клиента")
@allure.severity(allure.severity_level.NORMAL)
def test_update_existing_customer(connection, created_customer):
    """
    Фикстура created_customer уже создала клиента и гарантирует его удаление после теста.
    В этом тесте проверяем только логику update_customer → get_customer_by_id.
    """
    updated_data = {
        "firstname": "Updated",
        "lastname": "User",
        "email": generate_random_email(),
        "telephone": "9999999999",
    }

    with allure.step("Обновление данных клиента"):
        affected_rows = update_customer(connection, created_customer, updated_data)
        assert affected_rows == 1

    with allure.step("Проверка обновлённых данных"):
        customer = get_customer_by_id(connection, created_customer)
        for key, value in updated_data.items():
            assert customer[key] == value

@allure.feature("Клиенты")
@allure.story("Негативное обновление несуществующего клиента")
@allure.severity(allure.severity_level.MINOR)
def test_update_nonexistent_customer(connection):
    fake_id = 999999
    updated_data = {
        "firstname": "Ghost",
        "lastname": "User",
        "email": "ghost@example.com",
        "telephone": "0000000000"
    }

    with allure.step("Попытка обновить клиента с несуществующим ID"):
        affected_rows = update_customer(connection, fake_id, updated_data)
        assert affected_rows == 0

@allure.feature("Клиенты")
@allure.story("Удаление клиента")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_existing_customer(connection, created_customer):
    """
    Фикстура created_customer создала клиента заранее.
    В тесте проверяем, что delete_customer_by_id возвращает 1,
    и get_customer_by_id после удаления даёт None.
    Фикстура после теста повторно попытается удалить (что вернёт 0), но это безопасно.
    """
    with allure.step("Удаление клиента"):
        deleted = delete_customer_by_id(connection, created_customer)
        assert deleted == 1

    with allure.step("Проверка отсутствия клиента"):
        customer = get_customer_by_id(connection, created_customer)
        assert customer is None

@allure.feature("Клиенты")
@allure.story("Негативное удаление несуществующего клиента")
@allure.severity(allure.severity_level.MINOR)
def test_delete_nonexistent_customer(connection):
    fake_id = 999999
    with allure.step("Попытка удалить несуществующего клиента"):
        deleted = delete_customer_by_id(connection, fake_id)
        assert deleted == 0

@allure.feature("Клиенты")
@allure.story("Поиск клиента по email")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_customer_by_email(connection, created_customer, raw_customer_data):
    """
    Фикстура created_customer создала клиента с email из raw_customer_data.
    Проверяем get_customer_by_email возвращает правильную запись.
    """
    with allure.step("Поиск клиента по email"):
        customer = get_customer_by_email(connection, raw_customer_data["email"])
        assert customer is not None
        assert customer["customer_id"] == created_customer
        assert customer["email"] == raw_customer_data["email"]
        assert customer["firstname"] == raw_customer_data["firstname"]

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
def test_update_customer_status_existing(connection, created_customer):
    with allure.step("Изменение статуса клиента на 0 (неактивен)"):
        affected_rows = update_customer_status(connection, created_customer, 0)
        assert affected_rows == 1

    with allure.step("Проверка обновлённого статуса клиента"):
        customer = get_customer_by_id(connection, created_customer)
        assert customer is not None
        assert customer["status"] == 0

@allure.feature("Клиенты")
@allure.story("Обновление статуса несуществующего клиента")
@allure.severity(allure.severity_level.MINOR)
def test_update_customer_status_nonexistent(connection):
    fake_id = 999999

    with allure.step("Попытка обновить статус несуществующего клиента"):
        affected_rows = update_customer_status(connection, fake_id, 0)
        assert affected_rows == 0

    with allure.step("Проверка, что клиент не появился в базе"):
        customer = get_customer_by_id(connection, fake_id)
        assert customer is None

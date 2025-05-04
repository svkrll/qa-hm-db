import allure

@allure.feature("Подключение к базе данных")
@allure.severity(allure.severity_level.CRITICAL)
def test_connection_works(connection):
    with allure.step("Подключение к базе данных"):
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            assert "MariaDB" in version["VERSION()"] or "MySQL" in version["VERSION()"]

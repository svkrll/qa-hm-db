
def create_customer(connection, customer_data: dict) -> int:
    """
    Регистрирует нового клиента в таблице oc_customer.

    :param connection: соединение с базой данных PyMySQL
    :param customer_data: словарь с данными клиента
    :return: ID созданного клиента
    """
    query = """
        INSERT INTO oc_customer 
        (firstname, lastname, email, telephone, password, newsletter, status, date_added)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
    """
    
    params = (
        customer_data["firstname"],
        customer_data["lastname"],
        customer_data["email"],
        customer_data["telephone"],
        customer_data["password"],  # должен быть заранее хэширован
        customer_data.get("newsletter", 0),
        customer_data.get("status", 1),
    )

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        connection.commit()
        return cursor.lastrowid
    
def get_customer_by_email(connection, email: str) -> dict | None:
    """
    Получает информацию о клиенте по его email.

    :param connection: соединение с базой данных PyMySQL
    :param email: email клиента
    :return: словарь с данными клиента или None, если не найден
    """
    query = "SELECT * FROM oc_customer WHERE email = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result

def get_customer_by_id(connection, customer_id: int) -> dict | None:
    """
    Получает информацию о клиенте по его ID.

    :param connection: соединение с базой данных PyMySQL
    :param customer_id: ID клиента
    :return: словарь с данными клиента или None, если не найден
    """
    query = "SELECT * FROM oc_customer WHERE customer_id = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, (customer_id,))
        result = cursor.fetchone()
        return result


def delete_customer_by_id(connection, customer_id: int) -> int:
    """
    Удаляет клиента по его ID.

    :param connection: соединение с базой данных PyMySQL
    :param customer_id: ID клиента
    :return: количество удалённых строк (0 или 1)
    """
    query = "DELETE FROM oc_customer WHERE customer_id = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, (customer_id,))
        connection.commit()
        return cursor.rowcount
    
def update_customer_status(connection, customer_id: int, status: int) -> None:
    """
    Обновляет статус клиента (например, активен = 1, отключён = 0).

    :param connection: соединение с базой данных PyMySQL
    :param customer_id: ID клиента
    :param status: новый статус (0 = неактивен, 1 = активен)
    """
    query = "UPDATE oc_customer SET status = %s WHERE customer_id = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, (status, customer_id))
        connection.commit()

   
    

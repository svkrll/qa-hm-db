
def create_customer(connection, customer_data: dict) -> int:
    """
    Универсальная вставка записи в таблицу oc_customer без явного перечисления столбцов.
    :param connection: соединение с базой данных PyMySQL
    :param customer_data: словарь с данными клиента (все нужные поля)
    :return: ID созданного клиента
    """
    fields = ", ".join(customer_data.keys())
    placeholders = ", ".join(["%s"] * len(customer_data))
    values = tuple(customer_data.values())

    query = f"INSERT INTO oc_customer ({fields}) VALUES ({placeholders})"

    with connection.cursor() as cursor:
        cursor.execute(query, values)
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

def update_customer(connection, customer_id: int, updated_data: dict) -> int:
    if not updated_data:
        return 0

    set_clause = ", ".join([f"{key} = %s" for key in updated_data])
    values = list(updated_data.values()) + [customer_id]

    query = f"UPDATE oc_customer SET {set_clause} WHERE customer_id = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, values)
        connection.commit()
        return cursor.rowcount


def update_customer_status(connection, customer_id, new_status):
    """
    Обновляет поле status у клиента с заданным customer_id.
    Возвращает число строк, которые были затронуты запросом.
    """
    sql = "UPDATE oc_customer SET status = %s WHERE customer_id = %s"
    with connection.cursor() as cursor:
        affected_rows = cursor.execute(sql, (new_status, customer_id))
        connection.commit()
        return affected_rows

   
    

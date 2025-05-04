import pytest
import pymysql
from pymysql.cursors import DictCursor

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

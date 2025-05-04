#### opencart_db_framework
`docker-compose up -d` - запуск контейнеров

`PYTHONPATH=. pytest --host localhost --port 3306 --user bn_opencart  --database bitnami_opencart --alluredir allure-results` - запуск тестов
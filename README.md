# Django/DRF E-Commerce MarketPlace

### Первоначально нужно запустить контейнер с Postgresql
### `docker-compose up -d`
### После запуска потребуется установить все миграции из БД:
### `python3 manage.py makemigrations`
### `python3 manage.py migrate`
### Конечно не забываем про установку необходимых зависимостей:
### `pip install -r requirements.txt`
### Далее можно запустить сам веб-сервер:
### `python3 manage.py runserver`
### Веб-сервис будет находиться по адресу: http://localhost:8000/
### Чтобы завершить работу сервера нажмите комбинацию клавиш CTRL+C
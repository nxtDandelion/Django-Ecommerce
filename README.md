## Django/DRF E-Commerce MarketPlace

Первоначально нужно запустить контейнер с Postgresql <br>
`docker-compose up -d`<br>

После запуска потребуется установить все миграции из БД: <br>
`python3 manage.py makemigrations` <br>
`python3 manage.py migrate` <br>

Конечно не забываем про установку необходимых зависимостей: <br>
`pip install -r requirements.txt` <br>

Далее можно запустить сам веб-сервер: <br>
`python3 manage.py runserver` <br>

Веб-сервис будет находиться по адресу: http://localhost:8000/ <br>
SwaggerUI находится по адресу: http://localhost:8000/api/docs <br>

Чтобы завершить работу сервера нажмите комбинацию клавиш `CTRL+C` <br>
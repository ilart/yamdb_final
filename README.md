# yamdb_final

![YAMDB workflow](https://github.com/ilart/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

api для проекта yamdb. API позволяет создавать, удалять, получать и изменять записи в моделях. 
Подробности можно узнать в [документации](http://51.250.65.218/redoc/ "How to use API YAMDB")".

**Внимание, большинство операций трубуют аутентификацию пользователя.**

### Как запустить проект:

1. Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:ilart/yamdb_final.git
```

```bash
cd yamdb_final/infra
```

2. Заполнить файл с переменными окружения:

```bash
SECRET_KEY=SECRET_KEY
DB_NAME=NAME
DB_ENGINE=django.db.backends.postgresql
POSTGRES_USER=USERS
POSTGRES_PASSWORD=PASS
DB_HOST=localhost
DB_PORT=1234
```

3. Установите docker на сервер на котором планируется деплой.

```bash
sudo apt install docker.io 
```

4. Установите docker-compose, с этим вам поможет [официальная документация](https://docs.docker.com/compose/install/).

5. Скопируйте файлы docker-compose.yaml и nginx/default.conf из вашего 
проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно.

6. Добавьте в Secrets GitHub Actions переменные окружения:
- DOCKER_USERNAME 
- DOCKER_PASSWORD 
- DOCKER_USERNAME
- SSH_HOST 
- SSH_USER 
- SSH_KEY 
- DB_ENGINE 
- DB_NAME 
- POSTGRES_USER 
- POSTGRES_PASSWORD 
- DB_HOST 
- DB_PORT 
- TELEGRAM_TO 
- TELEGRAM_TOKEN 

7. Выполните git push на свой репозиторий. И убедитесь, что workflow завершился успешно.

8. Подключитесь к вашему серверу для дальнейшей донастройки.

8. Выполнить миграции, создайте пользователя и соберите статику для nginx:

```bash
docker-compose exec web python manage.py makemigrations users reviews api 
docker-compose exec web python manage.py migrate 
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic
```

5. Теперь проект готов.

6. Также вы можете загрузить данные из подготовленной базы:

```bash
docker cp ../fixtures.json infra_web_1:./
docker-compose exec web python manage.py loaddata /fixtures.json
```

## Используемые технологии

| Technology     | Description                   | Link ↘️                        |
|----------------|-------------------------------|--------------------------------|
| Django         | Фреймворк для веб-приложений  | https://www.djangoproject.com/ |
| Python3        | Интерпретатор языка Python3   | https://www.python.org/        |
| Nginx          | HTTP сервер                   | https://www.nginx.com/         |
| Docker         | Платформа для контейнеризации | https://docker.com/            |
| GitHub Actions | CI/CD платформа               | https://github.com/            |


## Автор
- github: ilart
- email: arteevilya@gmail.com 

## Ссылка на развернутый сервер
Здесь вы можете ознакомится и проверить как работает мой тестовый сервер:
- [Admin page](http://51.250.65.218/admin/)
- [Redoc](http://51.250.65.218/redoc/)
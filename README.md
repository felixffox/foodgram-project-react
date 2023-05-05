# Foodgram - Онлайн сервис для публикации рецептов.
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=013220)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=ffffff&color=013220)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=ffffff&color=013220)](https://www.django-rest-framework.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=ffffff&color=013220)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=ffffff&color=013220)](https://gunicorn.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=ffffff&color=013220)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=ffffff&color=013220)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=ffffff&color=013220)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=ffffff&color=013220)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=ffffff&color=013220)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=ffffff&color=013220)](https://cloud.yandex.ru/)

#### Статус проекта:
![example workflow](https://github.com/felixffox/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg)

#### Проект доступен по адресу:
[http://158.160.10.84]

## Описание проекта:
Это продуктовый помощник, сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Работа с API:
| Увидеть спецификацию API вы сможете по адресу | `.../api/docs/` |
|--------|:---------|
- Аутентификация выполняется с помощью djoser-токена.

### Доступные запросы:
| Запрос | Эндпоинт | Метод |
|--------|:---------|-------|
| Регистрация нового пользователя |`.../api/users/`| GET, POST |
| Запрос или сменна данных пользователя |`.../api/users/me/`| GET, POST |
| Запрос данных о пользователе |`.../api/users/{user_id}/`| GET |
| Получение токена (авторизация)|`.../api/auth/token/login/`| POST |
| Получение всех рецептов, создать новый рецепт|`.../api/recipes/`| GET, POST |
| Получение, редактирование, удаление рецепта по id|`.../api/recipes/`| GET, PUT, PATCH, DELETE |
| Список всех тегов|`.../api/tags/`| GET |
| Получение информации о теге по id|`.../api/tags/{tag_id}/`| GET |
| Получение списка всех ингредиентов|`.../api/igredients/`| GET |
| Получение информации о ингредиенте по id|`.../api/igredients/{igredient_id}/`| GET |
| Подписаться, отписаться или получить список всех избранных постов |`.../api/recipes/{recipes_id}/favorite`| GET, POST |
| Добавить, удалить или получить список всех рецептов в корзин |`.../api/recipes/{recipes_id}/favorite`| GET, POST |
| Получение списока ингредиентов в формате pdf|`.../api/recipes/download_shopping_cart`| GET |

## Инструкция по развёртыванию:
1. Загрузите проект.
```
git clone https://github.com/felixffox/foodgram-project-react.git
```
2. Подключиться к вашему серверу.
```
ssh <server user>@<server IP>
```
3. Установите Докер на свой сервер.
```
sudo apt install docker.io
```
4. Получить разрешения для docker-compose.
```
sudo chmod +x /usr/local/bin/docker-compose
```
5. Создайте каталог проекта.
```
mkdir foodgram && cd foodgram/
```
6. Создайте env-файл.
```
touch .env
```
7. Заполните env-файл.
```

SECRET_KEY = указываем секретный ключ
DB_ENGINE = указываем c тип БД 
DB_NAME = имя базы данных
POSTGRES_USER = логин для подключения к базе данных
POSTGRES_PASSWORD = пароль для подключения к БД (установите свой)
DB_HOST = название сервиса (контейнера)
DB_PORT = порт для подключения к БД
```
8. Скопируйте файлы из 'infra/' с ПК на ваш сервер.
```
scp infra/* <server user>@<server IP>:/home/<server user>/foodgram/
```
9. Запустите docker-compose.
```
sudo docker-compose up -d
```
10. Запустите миграции.
```
sudo docker-compose exec backend python manage.py migrate --noinput 
```
11. Запустите сбор статики.
```
sudo docker-compose exec backend python manage.py collectstatic --noinput
```
12. Создайте супер пользователя.

Например:

```
sudo docker-compose exec backend python manage.py createsuperuser

Username: Admin
Password: Admin
```

13. Загрузите данные в базу. Для этого в проект встроен механизм Import-Export. Таблицу ингредиентов из репозитория можно загрузить в базу данных прямо в панели администратора.

### Логин и пароль суперпользователя:
- username: Admin
- password: Admin

### Настроен Workflow и состоит из четрыех шагов:
- Проверка кода на соответствие PEP8
- Сборка и публикация образа бекенда на DockerHub.
- Автоматический деплой на удаленный сервер.
- Отправка уведомления в телеграм-чат.


### Бэкенд проекта реализовал:
[Вдовин Данил](https://github.com/felixffox)

# Учебный проект: сервис Foodgram

Проект позволяет пользователю публиковать рецепты своих блюд, читать рецепты других авторов, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в избранное и продуктовую корзину.  

## Ссылка на рабочий ресурс

http://51.250.29.38/

##

![example workflow](https://github.com/arche-ma/foodgram-project-react/actions/workflows/foodgram_workflow/badge.svg)


## Автор проекта
Луговик Сергей (@arche-ma)

## Техническое описание проекта
 
*запросы к API начинаются с `/api/`*
Полная документация возможных запросов API находится по адресу `api/docs`

Для работы с базой данных postgres необходимо создать файл .env, в котором будут указаны параметры базы данных и информация о пользователе. Файл необходимо разместить в директории 'backend/foodgram'

## Заполнение файла .env

Файл должен находиться в директории `backend/foodgram`

В файле необходимы следующие ключи:

DB_ENGINE=django.db.backends.postgresql

DB_NAME=postgres

POSTGRES_USER=**имя пользователя**

POSTGRES_PASSWORD=**пользовательский пароль**

DB_HOST=db

DB_PORT=5432


## Разворачивание проекта на локальной машине

Клонируем репозиторий на локальную машину:
 
```$ git clone https://github.com/arche-ma/foodgram-project-react```
 
В директории foodgram-project-react/infra выполняем команду:
 
 ```$ docker-compose up --build -d```
 
После разворачивания архитектуры проекта собираем статику, создаем миграции, заполняем таблицу ингредиентов и тэгов, создаем администратора. Все команды для этого находятся в скрипте `shortcut.sh`. Чтобы его запустить, выполним следующие команды:

```$ docker compose exec web sh ```

```$ ./shortcut.sh```

В конце выполнения скрипта необходимо будет ввести данные для аккаунта суперпользователя.

После выполнения этих шагов проект будет доступен по ссылке: `127.0.0.1/`
Панель администрирования находится по адресу `/admin/`

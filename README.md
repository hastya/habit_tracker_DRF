В 2018 году Джеймс Клир написал книгу «Атомные привычки», которая посвящена приобретению новых полезных привычек и
искоренению старых плохих привычек.
Реализован "Трекер полезных привычек" бэкенд-часть SPA веб-приложения.

<h1>Запуск проекта</h1>
python manage.py runserver

<h3>Настройка DRF в Docker</h3>
Клонировать проект: 

https://github.com/hastya/habit_tracker_DRF

<h3>Сборка без yaml файла</h3>

Сборка докер образа:

docker build -t my-python-app .

Запуск контейнера:

docker run my-python-app

<h3>Сборка с yaml файлом</h3>
Cоздание образа из Dockerfile:

docker-compose build

с запуском контейнера:

docker-compose up --build

с запуском конктейнера в фоновом режиме:

docker-compose up -d --build

Запуск контейнера:

docker-compose up

Миграции:

sudo docker-compose exec app python manage.py migrate
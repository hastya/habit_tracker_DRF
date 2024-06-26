# Используем базовый образ Python
FROM python:3

ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем зависимости в контейнер
COPY ./requirements.txt /app/

# Устанавливаем зависимости
RUN pip install -r /app/requirements.txt
RUN apt-get update && apt-get install -y postgresql-client

# Копируем код приложения в контейнер
COPY . .

# Команда для запуска приложения при старте контейнера
# CMD ["python", "manage.py", "runserver"]

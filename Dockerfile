# установка базового образа (host OS)
FROM python:3.11.7-slim-bullseye

# установка рабочей директории в контейнере
WORKDIR /app

# Устанавливаем временную зону
ENV TZ=Europe/Moscow

# копирование файла зависимостей в рабочую директорию
COPY requirements.txt .

# установка зависимостей
RUN pip install -r requirements.txt

# копирование содержимого локальной директории src в рабочую директорию
COPY src/ .

RUN mkdir -p /app/sessions

# команда, выполняемая при запуске контейнера
CMD [ "python", "main.py" ]

# Выкачиваем из dockerhub образ с python версии 3.9
FROM python:3.10-slim-buster
# Устанавливаем рабочую директорию для проекта в контейнере
WORKDIR /backend/python
# Скачиваем/обновляем необходимые библиотеки для проекта 
COPY requirements.txt /backend/python
RUN pip3 install --upgrade pip --proxy http://proxy.omgtu:8080 -r requirements.txt
# |ВАЖНЫЙ МОМЕНТ| копируем содержимое папки, где находится Dockerfile, 
# в рабочую директорию контейнера
COPY . /backend/python
# Устанавливаем порт, который будет использоваться для сервера
EXPOSE 5000
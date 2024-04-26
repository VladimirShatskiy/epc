# образ на основе которого создаём контейнер
FROM python:3.9-alpine

RUN mkdir app

# рабочая директория внутри проекта
WORKDIR /app

# переменные окружения для python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# устанавливаем зависимости
RUN pip install --upgrade pip
CMD ps
COPY requirements.txt .
RUN pip install -r requirements.txt

# port where the Django app runs
EXPOSE 2000

# копируем содержимое текущей папки в контейнер
COPY . /app

#ENTRYPOINT ["python", "manage.py" ]

#CMD ["sh", "-c", "python manage.py runserver -p2000:200 0.0.0.0:2000 ; python manage.py bot"]

#VOLUME /app/

# Используем базовый образ Python
FROM python:3.11

# Устанавливаем рабочую директорию контейнера
WORKDIR /app

# Устанавливаем зависимости из requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в рабочую директорию контейнера
COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

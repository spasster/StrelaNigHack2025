FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Создание директории для статических файлов
RUN mkdir -p /app/static

# Сборка статических файлов
RUN python manage.py collectstatic --noinput

# Открытие порта
EXPOSE 8000

# Запуск приложения
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"] 
FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Обновление pip
RUN pip install --upgrade pip

# Копирование файла зависимостей
COPY requirements.txt .

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Создание директории для статических файлов
RUN mkdir -p /app/static

# Установка переменных окружения
ENV DJANGO_SETTINGS_MODULE=backend.settings
ENV PYTHONUNBUFFERED=1

# Сборка статических файлов
RUN python manage.py collectstatic --noinput

# Открытие порта
EXPOSE 8000

# Запуск приложения
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"] 
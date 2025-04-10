# Этап сборки
FROM node:18-alpine

WORKDIR /app

# Копируем файлы зависимостей
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем исходный код
COPY . .

# Собираем приложение
RUN npm run build

# Установка nginx и необходимых инструментов
RUN apk add --no-cache nginx net-tools

# Создаем необходимые директории для nginx
RUN mkdir -p /usr/share/nginx/html && \
    mkdir -p /var/log/nginx && \
    mkdir -p /var/run && \
    mkdir -p /etc/nginx

# Копируем конфигурацию Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Копируем собранное приложение в директорию nginx
RUN cp -r .output/public/* /usr/share/nginx/html/ && \
    chmod -R 755 /usr/share/nginx/html && \
    chown -R nginx:nginx /usr/share/nginx/html

# Создаем и настраиваем логи
RUN touch /var/log/nginx/access.log && \
    touch /var/log/nginx/error.log && \
    chmod 644 /var/log/nginx/*.log && \
    chown -R nginx:nginx /var/log/nginx

# Открываем порт
EXPOSE 80

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"] 
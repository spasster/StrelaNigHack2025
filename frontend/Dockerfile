# Шаг сборки приложения
FROM node:22-alpine AS builder

WORKDIR /app

# Копируем файлы зависимостей
COPY package*.json ./
COPY .npmrc* ./

# Устанавливаем зависимости
RUN npm install --frozen-lockfile

# Копируем исходный код
COPY . .

# Собираем приложение
RUN npm run build

# Финальный образ с Nginx
FROM nginx:alpine

# Копируем собранное приложение из builder
COPY --from=builder /app/.output /usr/share/nginx/html

# Копируем конфигурацию Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Открываем порт 80
EXPOSE 80

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"]
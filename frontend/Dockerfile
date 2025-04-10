# Используем официальный образ для Node.js
FROM node:22-alpine

# Определяем аргумент для API URL
ARG NUXT_PUBLIC_API_URL

# Делаем его переменной окружения внутри контейнера
ENV NUXT_PUBLIC_API_URL=${NUXT_PUBLIC_API_URL}

# Рабочая директория
WORKDIR /app

# Копируем package.json и package-lock.json
COPY frontend/package.json frontend/package-lock.json ./

# Устанавливаем зависимости с помощью npm
RUN npm install

# Копируем весь код
COPY frontend/ .

# Собираем Nuxt
RUN npm run build

# Открываем порт для приложения
EXPOSE 3000

# Запускаем Nuxt
CMD ["npm", "preview"]
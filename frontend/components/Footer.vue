<template>
  <footer class="bg-gray-900 text-white py-12">
    <div class="container mx-auto px-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- О компании -->
        <div>
          <h3 class="text-xl font-bold mb-4">О нас</h3>
          <p class="text-gray-400">
            Современный отель с комфортабельными номерами и высоким уровнем сервиса.
            Мы создаем уютную атмосферу для каждого гостя.
          </p>
        </div>

        <!-- Контакты -->
        <div>
          <h3 class="text-xl font-bold mb-4">Контакты</h3>
          <ul class="space-y-2 text-gray-400">
            <li class="flex items-center">
              <i class="pi pi-map-marker mr-2"></i>
              г. Москва, ул. Примерная, 123
            </li>
            <li class="flex items-center">
              <i class="pi pi-phone mr-2"></i>
              +7 (999) 123-45-67
            </li>
            <li class="flex items-center">
              <i class="pi pi-envelope mr-2"></i>
              info@hotel-example.ru
            </li>
          </ul>
        </div>

        <!-- Быстрые ссылки -->
        <div>
          <h3 class="text-xl font-bold mb-4">Навигация</h3>
          <ul class="space-y-2 text-gray-400">
            <li>
              <NuxtLink to="/" class="hover:text-white transition-colors">
                Главная
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/hotel-map" class="hover:text-white transition-colors">
                Выбор номера
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/about" class="hover:text-white transition-colors">
                О нас
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/contacts" class="hover:text-white transition-colors">
                Контакты
              </NuxtLink>
            </li>
          </ul>
        </div>

        <!-- Социальные сети -->
        <div>
          <h3 class="text-xl font-bold mb-4">Мы в соцсетях</h3>
          <div class="flex space-x-4">
            <a href="#" class="text-gray-400 hover:text-white transition-colors">
              <i class="pi pi-facebook text-2xl"></i>
            </a>
            <a href="#" class="text-gray-400 hover:text-white transition-colors">
              <i class="pi pi-instagram text-2xl"></i>
            </a>
            <a href="#" class="text-gray-400 hover:text-white transition-colors">
              <i class="pi pi-telegram text-2xl"></i>
            </a>
            <a href="#" class="text-gray-400 hover:text-white transition-colors">
              <i class="pi pi-vk text-2xl"></i>
            </a>
          </div>
        </div>
      </div>

      <!-- Нижняя часть футера -->
      <div class="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
        <p>&copy; {{ new Date().getFullYear() }} Отель "Пример". Все права защищены.</p>
      </div>
    </div>
  </footer>
</template>

<script lang="ts" setup>
</script>

<style scoped>
.font-paratype {
  font-family: 'ParaType', sans-serif;
}
</style>
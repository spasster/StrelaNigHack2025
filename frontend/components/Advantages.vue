<template>
  <section class="relative py-16 md:py-24 overflow-hidden">
    <!-- Декоративные элементы -->
    <img src="/advantages1.svg" alt="" class="absolute top-0 left-0 w-[50%]" />
    <img src="/advantages1.svg" alt="" class="absolute bottom-0 right-0  w-[50%] transform scale-y-[-1] scale-x-[-1]" />
    
    <div class="container mx-auto px-4 md:px-10 lg:px-20">
      <h2 class="text-3xl md:text-4xl font-bold text-center mb-12">
        Почему выбирают нас
      </h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <!-- Удобство -->
        <div class="bg-custom-card p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h3 class="text-xl font-semibold mb-2">Удобство</h3>
          <p class="text-white/80">Интуитивно понятный интерфейс и быстрый доступ ко всем необходимым функциям. Забудьте о сложностях - мы сделали всё максимально просто.</p>
        </div>

        <!-- Безопасность -->
        <div class="bg-custom-card p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <h3 class="text-xl font-semibold mb-2">Безопасность</h3>
          <p class="text-white/80">Современные технологии шифрования и защиты данных. Ваша информация всегда под надёжной защитой.</p>
        </div>

        <!-- Доступность -->
        <div class="bg-custom-card p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-xl font-semibold mb-2">Доступность</h3>
          <p class="text-white/80">Работайте с нами из любой точки мира. Наш сервис доступен 24/7 на всех устройствах.</p>
        </div>

        <!-- Простота -->
        <div class="bg-custom-card p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
          <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h3 class="text-xl font-semibold mb-2">Простота</h3>
          <p class="text-white/80">Минимум действий для достижения результата. Мы убрали всё лишнее, оставив только необходимое.</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// Компонент не требует дополнительной логики
</script> 
<template>
  <section class="w-full h-screen absolute top-0 left-0 -z-10">
    <div class="max-w-7xl gap-x-4 mx-auto px-4 pt-28 pb-10 md:px-6 flex flex-col md:flex-row items-center md:justify-between w-full h-full">
      <!-- Левая часть с текстом -->
      <div class="flex flex-col gap-6 md:gap-8 max-w-xl text-center md:text-left">
        <h1 class="text-3xl md:text-5xl font-bold text-white">
          Добро пожаловать в Strela
        </h1>
        <p class="text-base md:text-lg text-white/80">
          Откройте для себя уютные номера и незабываемый отдых в нашем отеле. 
          Мы предлагаем комфортное размещение и высокий уровень сервиса.
        </p>
        <CustomButton>
          Просмотр комнат
        </CustomButton>
      </div>

      <!-- Правая часть с картинкой -->
      <div class="relative w-full h-full md:w-auto mt-8 md:mt-0">
        <img 
          src="/index.png" 
          alt="Hotel Room" 
          class="w-full md:w-[600px] h-full md:h-[600px] object-cover rounded-bl-[50px] md:rounded-bl-[100px]"
        />
      </div>
    </div>
  </section>
</template>

<script lang="ts" setup>
import CustomButton from './CustomButton.vue'
</script> 
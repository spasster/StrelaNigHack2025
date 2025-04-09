<template>
  <section class="w-full h-full flex justify-center items-center relative">
    <div class="w-full h-[90vh] gap-x-4 mx-auto px-4 pt-10 pb-10 md:px-6 flex flex-col md:flex-row items-center md:justify-between">
      <!-- Левая часть с текстом -->
      <div class="flex flex-col gap-6 md:gap-8 max-w-xl text-center md:text-left">
        <h1 class="text-3xl md:text-5xl font-bold text-white">
          Добро пожаловать в Strela
        </h1>
        <p class="text-base md:text-lg text-white/80">
          Откройте для себя уютные номера и незабываемый отдых в нашем отеле. 
          Мы предлагаем комфортное размещение и высокий уровень сервиса.
        </p>
        <NuxtLink to="/catalog" class="w-full mx-auto md:mx-0">
          <CustomButton class="w-full">
            Просмотр комнат
          </CustomButton>
        </NuxtLink>
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
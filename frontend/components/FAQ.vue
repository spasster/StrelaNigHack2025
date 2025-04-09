<template>
  <div class="container mx-auto p-4 py-10">
    <h2 class="text-4xl font-bold text-center mb-8 text-white">Часто задаваемые вопросы</h2>
    
    <div class="space-y-4 max-w-3xl mx-auto">
      <div 
        v-for="(item, index) in faqItems" 
        :key="index"
        class="bg-custom-card rounded-lg overflow-hidden transition-all duration-300"
        :class="{ 'shadow-lg': activeIndex === index }"
      >
        <button
          @click="toggleAccordion(index)"
          class="w-full p-4 text-left flex items-center justify-between hover:bg-gray-700/50 transition-colors duration-200"
        >
          <span class="text-white font-medium text-lg">{{ item.question }}</span>
          <div class="transform transition-transform duration-300" :class="{ 'rotate-180': activeIndex === index }">
            <svg 
              class="w-6 h-6 text-custom-yellow" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </button>
        
        <div 
          class="overflow-hidden transition-all duration-300"
          :style="{ 
            maxHeight: activeIndex === index ? '500px' : '0px',
            opacity: activeIndex === index ? 1 : 0
          }"
        >
          <div class="p-4 pt-0 text-white/80">
            {{ item.answer }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const activeIndex = ref<number | null>(null);

const faqItems = [
  {
    question: 'Как забронировать номер?',
    answer: 'Для бронирования номера необходимо зарегистрироваться на сайте, выбрать подходящий номер и заполнить форму бронирования. После подтверждения бронирования вы получите уведомление на email.'
  },
  {
    question: 'Какие документы нужны для заселения?',
    answer: 'При заселении необходимо предъявить паспорт, студенческий билет и договор о проживании. Для иностранных студентов дополнительно требуется миграционная карта.'
  },
  {
    question: 'Можно ли заселиться раньше/позже указанного времени?',
    answer: 'Да, раннее заселение и поздний выезд возможны по предварительной договоренности. Дополнительная плата за раннее заселение/поздний выезд не взимается.'
  },
  {
    question: 'Есть ли скидки для студентов?',
    answer: 'Да, для студентов действуют специальные тарифы. Также предусмотрены скидки при долгосрочном проживании и при бронировании нескольких номеров для группы студентов.'
  },
  {
    question: 'Какие удобства есть в номерах?',
    answer: 'Все номера оборудованы современной мебелью, кондиционером, телевизором, холодильником и беспроводным интернетом. В каждом номере есть отдельная ванная комната с душем.'
  },
  {
    question: 'Можно ли приглашать гостей?',
    answer: 'Да, гости могут посещать проживающих с 8:00 до 23:00. При этом необходимо предупредить администрацию и зарегистрировать гостя на ресепшене.'
  }
];

const toggleAccordion = (index: number) => {
  activeIndex.value = activeIndex.value === index ? null : index;
};
</script>

<style scoped>
.bg-custom-card {
  background: rgba(31, 41, 55, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.rotate-180 {
  transform: rotate(180deg);
}

.shadow-lg {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}
</style> 
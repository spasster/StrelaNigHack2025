<template>
  <div class="container mx-auto p-4 min-h-screen">
    <h1 class="text-2xl font-bold text-center mb-8 text-white">Контакты</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
      <!-- Контактная информация -->
      <div class="bg-custom-card p-6 rounded-lg shadow-lg">
        <h2 class="text-xl font-semibold text-white mb-4">Контактная информация</h2>
        <div class="space-y-4">
          <div class="flex items-start gap-3">
            <i class="pi pi-map-marker text-blue-400 mt-1"></i>
            <div>
              <h3 class="text-white font-medium">Адрес</h3>
              <p class="text-white/80">г. Москва, ул. Студенческая, д. 1</p>
            </div>
          </div>
          <div class="flex items-start gap-3">
            <i class="pi pi-phone text-blue-400 mt-1"></i>
            <div>
              <h3 class="text-white font-medium">Телефон</h3>
              <p class="text-white/80">+7 (495) 123-45-67</p>
            </div>
          </div>
          <div class="flex items-start gap-3">
            <i class="pi pi-envelope text-blue-400 mt-1"></i>
            <div>
              <h3 class="text-white font-medium">Email</h3>
              <p class="text-white/80">info@studenthotel.ru</p>
            </div>
          </div>
          <div class="flex items-start gap-3">
            <i class="pi pi-clock text-blue-400 mt-1"></i>
            <div>
              <h3 class="text-white font-medium">Режим работы</h3>
              <p class="text-white/80">Круглосуточно, без выходных</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Форма обратной связи -->
      <div class="bg-custom-card p-6 rounded-lg shadow-lg">
        <h2 class="text-xl font-semibold text-white mb-4">Обратная связь</h2>
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-white/80 mb-1">Имя</label>
            <InputText 
              v-model="form.name" 
              class="w-full bg-gray-700 border-none text-white"
              placeholder="Введите ваше имя"
            />
          </div>
          <div>
            <label class="block text-white/80 mb-1">Email</label>
            <InputText 
              v-model="form.email" 
              class="w-full bg-gray-700 border-none text-white"
              placeholder="Введите ваш email"
            />
          </div>
          <div>
            <label class="block text-white/80 mb-1">Сообщение</label>
            <Textarea 
              v-model="form.message" 
              class="w-full bg-gray-700 border-none text-white"
              placeholder="Введите ваше сообщение"
              rows="5"
            />
          </div>
          <CustomButton 
            type="submit" 
            class="w-full"
            :loading="isSubmitting"
          >
            Отправить
          </CustomButton>
        </form>
      </div>
    </div>

    <!-- Карта -->
    <div class="bg-custom-card p-6 rounded-lg shadow-lg">
      <h2 class="text-xl font-semibold text-white mb-4">Как нас найти</h2>
      <div class="aspect-video w-full">
        <iframe 
          src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2245.371787409134!2d37.6176333!3d55.755826!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46b54a50b315e573%3A0xa886bf5a3d9b2e68!2z0JzQvtGB0LrQvtCy0YHQutC40Lkg0JrRgNC10LzQu9GM!5e0!3m2!1sru!2sru!4v1647781234567!5m2!1sru!2sru" 
          class="w-full h-full rounded-lg"
          style="border:0;" 
          allowfullscreen="true" 
          loading="lazy"
        ></iframe>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useToast } from 'primevue/usetoast';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import CustomButton from '~/components/CustomButton.vue';

const toast = useToast();
const isSubmitting = ref(false);

const form = ref({
  name: '',
  email: '',
  message: ''
});

const handleSubmit = async () => {
  try {
    isSubmitting.value = true;
    // Здесь будет логика отправки формы
    await new Promise(resolve => setTimeout(resolve, 1000)); // Имитация запроса
    
    toast.add({
      severity: 'success',
      summary: 'Успешно',
      detail: 'Ваше сообщение отправлено',
      life: 3000,
    });
    
    form.value = {
      name: '',
      email: '',
      message: ''
    };
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось отправить сообщение',
      life: 3000,
    });
  } finally {
    isSubmitting.value = false;
  }
};
</script> 
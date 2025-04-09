<template>
  <div class="container mx-auto p-4 min-h-screen">
    <h1 class="text-2xl font-bold text-center mb-8 text-white">Профиль</h1>
    
    <div v-if="isLoading" class="flex justify-center items-center min-h-[60vh]">
      <div class="flex flex-col items-center gap-4">
        <ProgressSpinner 
          strokeWidth="4" 
          class="w-16 h-16"
          :class="{ 'w-12 h-12': isMobile }"
        />
        <p class="text-white/60">Загрузка данных профиля...</p>
      </div>
    </div>

    <div v-else class="flex flex-col lg:flex-row gap-8">
      <!-- Карточка пользователя -->
      <div class="w-full lg:w-1/3">
        <div 
          class="relative w-full aspect-[1.6] cursor-pointer transition-transform duration-500 transform-gpu"
          :class="{ 'rotate-y-180': isFlipped }"
          @mouseenter="!isMobile && (isFlipped = true)"
          @mouseleave="!isMobile && (isFlipped = false)"
          @click="handleCardClick"
        >
          <!-- Передняя сторона -->
          <div class="absolute w-full h-full backface-hidden z-10">
            <img 
              src="/card-front.svg" 
              alt="Лицевая сторона карты" 
              class="w-full h-full rounded-lg shadow-lg"
            />
          </div>
          
          <!-- Задняя сторона -->
          <div class="absolute w-full h-full backface-hidden" style="transform: rotateY(180deg);">
            <img 
              src="/card-back.svg" 
              alt="Обратная сторона карты" 
              class="w-full h-full rounded-lg shadow-lg"
            />
            <!-- QR код -->
            <div class="absolute top-[45%] left-1/4 transform -translate-x-1/2 -translate-y-1/2 z-20">
              <div @click.stop="showQrModal = true" class="cursor-pointer">
                <QRCodeVue 
                  :value="qrCodeUrl" 
                  :size="qrCodeSize"
                  level="H"
                  render-as="canvas"
                  class="bg-white p-2 rounded"
                />
                <p class="text-white text-center mt-2" :class="{ 'text-sm': isMobile }">
                  Увеличить
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Информация о пользователе -->
      <div class="flex-1 bg-custom-card p-6 rounded-lg shadow-lg">
        <h2 class="text-xl font-semibold text-white mb-6">Личная информация</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-4">
            <div>
              <label class="block text-white/80 mb-1">Имя</label>
              <div class="bg-gray-700 text-white p-2 rounded">{{ userData.name || 'Не указано' }}</div>
            </div>
            <div>
              <label class="block text-white/80 mb-1">Фамилия</label>
              <div class="bg-gray-700 text-white p-2 rounded">{{ userData.surname || 'Не указано' }}</div>
            </div>
            <div>
              <label class="block text-white/80 mb-1">Отчество</label>
              <div class="bg-gray-700 text-white p-2 rounded">{{ userData.fathername || 'Не указано' }}</div>
            </div>
            <div>
              <label class="block text-white/80 mb-1">Email</label>
              <div class="bg-gray-700 text-white p-2 rounded">{{ userData.email || 'Не указано' }}</div>
            </div>
          </div>
          
          <div class="space-y-4">
            <div>
              <label class="block text-white/80 mb-1">Телефон</label>
              <div class="bg-gray-700 text-white p-2 rounded">{{ userData.phone_number || 'Не указано' }}</div>
            </div>
            <div>
              <label class="block text-white/80 mb-1">Дата рождения</label>
              <div class="bg-gray-700 text-white p-2 rounded">{{ formatDate(userData.birth_date) || 'Не указано' }}</div>
            </div>
            <div>
              <label class="block text-white/80 mb-1">Университет</label>
              <div class="bg-gray-700 text-white p-2 rounded">{{ userData.university || 'Не указано' }}</div>
            </div>
            <div>
              <label class="block text-white/80 mb-1">Факультет</label>
              <div class="bg-gray-700 text-white p-2 rounded">{{ userData.faculty || 'Не указано' }}</div>
            </div>
            <div>
              <label class="block text-white/80 mb-1">Курс</label>
              <div class="bg-gray-700 text-white p-2 rounded">{{ userData.course || 'Не указано' }}</div>
            </div>
            <div>
              <label class="block text-white/80 mb-1">Номер комнаты</label>
              <div class="bg-gray-700 text-white p-2 rounded">{{ userData.room || 'Не указано' }}</div>
            </div>
          </div>
        </div>

        <!-- Информация о бронировании -->
        <div v-if="userData.check_in_date || userData.check_out_date" class="mt-8">
          <h2 class="text-xl font-semibold text-white mb-6">Информация о бронировании</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-white/80 mb-1">Дата заезда</label>
              <div class="bg-gray-700 text-white p-2 rounded">{{ formatDateTime(userData.check_in_date) || 'Не указано' }}</div>
            </div>
            <div>
              <label class="block text-white/80 mb-1">Дата выезда</label>
              <div class="bg-gray-700 text-white p-2 rounded">{{ formatDateTime(userData.check_out_date) || 'Не указано' }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно с QR кодом -->
    <Dialog
      v-model:visible="showQrModal"
      modal
      :style="{ width: '450px' }"
      class="bg-custom-card border-none font-paratype mx-2"
      @click="showQrModal = false"
    >
      <template #header>
        <h2 class="text-xl text-white font-semibold">QR код</h2>
      </template>

      <div class="flex flex-col items-center gap-4">
        <QRCodeVue 
          :value="qrCodeUrl" 
          :size="modalQrCodeSize"
          level="H"
          render-as="canvas"
          class="bg-white p-4 rounded"
        />
        <p class="text-white/60 text-center" :class="{ 'text-sm': isMobile }">
          Отсканируйте QR-код для быстрого доступа к профилю
        </p>
      </div>

      <template #footer>
        <CustomButton
          class="w-full"
          @click="showQrModal = false"
        >Закрыть</CustomButton>
      </template>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useToast } from 'primevue/usetoast';
import { useAuthStore } from '~/stores/auth'
import { useFetch } from '~/composables/useFetch'
import QRCodeVue from 'qrcode.vue'
import Dialog from 'primevue/dialog';
import ProgressSpinner from 'primevue/progressspinner';
import CustomButton from '~/components/CustomButton.vue';

const toast = useToast();
const isMobile = ref(false);
const isFlipped = ref(false);
const showQrModal = ref(false);
const isLoading = ref(true);
const qrCodeSize = computed(() => isMobile.value ? 80 : 120);
const modalQrCodeSize = computed(() => isMobile.value ? 200 : 256);
const userData = ref({
  name: '',
  surname: '',
  fathername: '',
  email: '',
  phone_number: '',
  birth_date: '',
  university: '',
  faculty: '',
  course: '',
  room: '',
  check_in_date: '',
  check_out_date: '',
  id: ''
});

const authStore = useAuthStore();
const { fetchWithAuth } = useFetch();

// Генерация QR кода
const qrCodeUrl = computed(() => {
  return `https://imgur.com/gc9racx`;
});

// Форматирование даты
const formatDate = (dateString: string) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU');
};

// Форматирование даты и времени
const formatDateTime = (dateString: string) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// Загрузка данных пользователя
const loadUserData = async () => {
  try {
    isLoading.value = true;
    const response = await fetchWithAuth('/api/auth/profile/');
    if (!response.ok) {
      throw new Error('Ошибка загрузки данных');
    }
    const data = await response.json();
    userData.value = data;
  } catch (error) {
    console.error('Ошибка загрузки профиля:', error);
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось загрузить данные профиля',
      life: 3000,
    });
  } finally {
    isLoading.value = false;
  }
};

// Проверяем мобильное устройство
onMounted(() => {
  isMobile.value = window.innerWidth <= 768;
  window.addEventListener('resize', () => {
    isMobile.value = window.innerWidth <= 768;
  });
  loadUserData();
});

// Обработчик клика для мобильных устройств
const handleCardClick = () => {
  if (isMobile.value) {
    isFlipped.value = !isFlipped.value;
  }
};
</script>

<style scoped>
.backface-hidden {
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  position: absolute;
  width: 100%;
  height: 100%;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.rotate-y-180 {
  transform: rotateY(180deg);
  -webkit-transform: rotateY(180deg);
}

/* Контейнер для карточки */
.relative {
  perspective: 1000px;
  transform-style: preserve-3d;
}

/* Стили для мобильных устройств */
@media (max-width: 768px) {
  .container {
    padding: 1rem;
  }
  
  .backface-hidden {
    transition: transform 0.4s;
  }
}
</style>
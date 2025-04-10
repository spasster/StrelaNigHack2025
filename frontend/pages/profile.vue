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

        <!-- Секция подписок и оплат -->
        <div class="mt-8">
          <div class="bg-custom-card p-6 rounded-lg shadow-lg">
            <h2 class="text-xl font-semibold text-white mb-6">Подписки и оплаты</h2>
            
            <!-- Активные подписки -->
            <div class="mb-6">
              <h3 class="text-lg font-medium text-white mb-4">Активные подписки</h3>
              <div v-if="activeSubscriptions.length" class="space-y-4">
                <div v-for="subscription in activeSubscriptions" :key="subscription.id" 
                     class="bg-gray-700 p-4 rounded-lg">
                  <div class="flex justify-between items-center">
                    <div>
                      <p class="text-white font-medium">{{ subscription.bill_type === 'SUBSCRIPTION' ? 'Подписка' : 'Аренда' }}</p>
                      <p class="text-white/60 text-sm">Срок: {{ formatDate(subscription.rent_start_date) }} - {{ formatDate(subscription.rent_end_date) }}</p>
                    </div>
                    <div class="text-right">
                      <p class="text-white font-medium">{{ subscription.amount }} ₽</p>
                      <p class="text-sm" :class="{
                        'text-green-400': subscription.status === 'PAID',
                        'text-yellow-400': subscription.status === 'PENDING',
                        'text-red-400': subscription.status === 'OVERDUE'
                      }">
                        {{ getStatusText(subscription.status) }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              <p v-else class="text-white/60">Нет активных подписок</p>
            </div>

            <!-- Продление подписки -->
            <div class="mb-6">
              <h3 class="text-lg font-medium text-white mb-4">Продлить подписку</h3>
              <div class="space-y-4">
                <div class="bg-gray-700 p-4 rounded-lg">
                  <div class="flex justify-between items-center mb-4">
                    <div>
                      <p class="text-white font-medium">Месячная подписка</p>
                      <p class="text-white/60 text-sm">Доступ ко всем функциям</p>
                    </div>
                    <p class="text-white font-medium">5000 ₽</p>
                  </div>
                  <CustomButton 
                    class="w-full"
                    @click="createSubscription('MONTH')"
                  >
                    Продлить на месяц
                  </CustomButton>
                </div>

                <div class="bg-gray-700 p-4 rounded-lg">
                  <div class="flex justify-between items-center mb-4">
                    <div>
                      <p class="text-white font-medium">Семестровая подписка</p>
                      <p class="text-white/60 text-sm">Доступ ко всем функциям</p>
                    </div>
                    <p class="text-white font-medium">25000 ₽</p>
                  </div>
                  <CustomButton 
                    class="w-full"
                    @click="createSubscription('SEMESTER')"
                  >
                    Продлить на семестр
                  </CustomButton>
                </div>

                <div class="bg-gray-700 p-4 rounded-lg">
                  <div class="flex justify-between items-center mb-4">
                    <div>
                      <p class="text-white font-medium">Годовая подписка</p>
                      <p class="text-white/60 text-sm">Доступ ко всем функциям</p>
                    </div>
                    <p class="text-white font-medium">45000 ₽</p>
                  </div>
                  <CustomButton 
                    class="w-full"
                    @click="createSubscription('YEAR')"
                  >
                    Продлить на год
                  </CustomButton>
                </div>
              </div>
            </div>

            <!-- История платежей -->
            <div>
              <h3 class="text-lg font-medium text-white mb-4">История платежей</h3>
              <div v-if="paymentHistory.length" class="space-y-4">
                <div v-for="payment in paymentHistory" :key="payment.id" 
                     class="bg-gray-700 p-4 rounded-lg">
                  <div class="flex justify-between items-center">
                    <div>
                      <p class="text-white font-medium">{{ formatDate(payment.payment_date) }}</p>
                      <p class="text-white/60 text-sm">{{ getPaymentMethodText(payment.payment_method) }}</p>
                    </div>
                    <div class="text-right">
                      <p class="text-white font-medium">{{ payment.amount }} ₽</p>
                      <p class="text-sm" :class="{
                        'text-green-400': payment.status === 'SUCCESS',
                        'text-yellow-400': payment.status === 'PENDING',
                        'text-red-400': payment.status === 'FAILED'
                      }">
                        {{ getPaymentStatusText(payment.status) }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              <p v-else class="text-white/60">Нет истории платежей</p>
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

interface Subscription {
  id: number;
  bill_type: 'SUBSCRIPTION' | 'RENT';
  rent_start_date: string;
  rent_end_date: string;
  amount: string;
  status: 'PAID' | 'PENDING' | 'OVERDUE' | 'CANCELLED';
}

interface Payment {
  id: number;
  payment_date: string;
  payment_method: 'CARD' | 'CASH' | 'TRANSFER';
  amount: string;
  status: 'SUCCESS' | 'PENDING' | 'FAILED';
}

const activeSubscriptions = ref<Subscription[]>([])
const paymentHistory = ref<Payment[]>([])

// Генерация QR кода
const qrCodeUrl = computed(() => {
  const accessToken = authStore.accessToken;
  return `https://neimarl-aparts/check/${accessToken}`;
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

// Загрузка данных о подписках и платежах
const loadBillsData = async () => {
  try {
    // Загрузка активных подписок
    const subscriptionsResponse = await fetchWithAuth('/api/bills/bills/')
    if (subscriptionsResponse.ok) {
      const data = await subscriptionsResponse.json()
      activeSubscriptions.value = data.filter((bill: Subscription) => 
        bill.bill_type === 'SUBSCRIPTION' && 
        bill.status !== 'CANCELLED'
      )
    }

    // Загрузка истории платежей
    const paymentsResponse = await fetchWithAuth('/api/bills/payments/')
    if (paymentsResponse.ok) {
      paymentHistory.value = await paymentsResponse.json()
    }
  } catch (error) {
    console.error('Ошибка загрузки данных о подписках и платежах:', error)
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось загрузить данные о подписках и платежах',
      life: 3000,
    })
  }
}

// Создание новой подписки
const createSubscription = async (period: string) => {
  try {
    // Определяем сумму в зависимости от периода
    const amount = period === 'MONTH' ? '15000.00' : 
                  period === 'SEMESTER' ? '25000.00' : 
                  '45000.00'

    // Получаем текущую дату
    const today = new Date()
    const rentStartDate = today.toISOString().split('T')[0]

    const response = await fetchWithAuth('/api/bills/rent/create/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        subscription_period: period,
        amount: amount,
        rent_start_date: rentStartDate
      })
    })

    if (response.ok) {
      const data = await response.json()
      // Перенаправляем на страницу оплаты
      window.location.href = data.bill.payment_url
    } else {
      throw new Error('Ошибка при создании подписки')
    }
  } catch (error) {
    console.error('Ошибка при создании подписки:', error)
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось создать подписку',
      life: 3000,
    })
  }
}

// Вспомогательные функции для отображения статусов
const getStatusText = (status: string) => {
  switch (status) {
    case 'PAID': return 'Оплачено'
    case 'PENDING': return 'Ожидает оплаты'
    case 'OVERDUE': return 'Просрочено'
    default: return status
  }
}

const getPaymentMethodText = (method: string) => {
  switch (method) {
    case 'CARD': return 'Банковская карта'
    case 'CASH': return 'Наличные'
    case 'TRANSFER': return 'Банковский перевод'
    default: return method
  }
}

const getPaymentStatusText = (status: string) => {
  switch (status) {
    case 'SUCCESS': return 'Успешно'
    case 'PENDING': return 'В обработке'
    case 'FAILED': return 'Ошибка'
    default: return status
  }
}

// Проверяем мобильное устройство
onMounted(() => {
  isMobile.value = window.innerWidth <= 768;
  window.addEventListener('resize', () => {
    isMobile.value = window.innerWidth <= 768;
  });
  loadUserData();
  loadBillsData();
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
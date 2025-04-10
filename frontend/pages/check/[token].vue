<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 flex items-center justify-center p-4">
    <div class="max-w-md w-full">
      <!-- Логотип -->
      <div class="text-center mb-8">
        <img src="/logo.png" alt="Logo" class="h-8 mx-auto mb-4">
        <h1 class="text-2xl font-bold text-white">Проверка подписки</h1>
      </div>

      <!-- Карточка статуса -->
      <div class="bg-custom-card rounded-lg shadow-xl p-8 mb-8">
        <div v-if="isLoading" class="flex flex-col items-center">
          <ProgressSpinner 
            strokeWidth="4" 
            class="w-12 h-12 mb-4"
          />
          <p class="text-white/60">Проверяем статус подписки...</p>
        </div>

        <div v-else-if="error" class="text-center">
          <div class="text-red-400 mb-4">
            <i class="pi pi-exclamation-triangle text-4xl"></i>
          </div>
          <h2 class="text-xl font-semibold text-white mb-2">Ошибка</h2>
          <p class="text-white/60">{{ error }}</p>
        </div>

        <div v-else class="text-center">
          <div :class="{
            'text-green-400': hasActiveSubscription,
            'text-yellow-400': !hasActiveSubscription
          }" class="mb-4">
            <i :class="{
              'pi pi-check-circle': hasActiveSubscription,
              'pi pi-exclamation-circle': !hasActiveSubscription
            }" class="text-4xl"></i>
          </div>
          
          <h2 class="text-xl font-semibold text-white mb-2">
            {{ hasActiveSubscription ? 'Подписка активна' : 'Подписка неактивна' }}
          </h2>
          
          <p class="text-white/60 mb-4">
            {{ hasActiveSubscription 
              ? 'Ваша подписка действительна и активна' 
              : 'У вас нет активной подписки' 
            }}
          </p>

          <div v-if="subscriptionDetails" class="bg-gray-700 rounded-lg p-4 mb-4">
            <div class="flex justify-between items-center mb-2">
              <span class="text-white/60">Тип подписки:</span>
              <span class="text-white font-medium">
                {{ getSubscriptionTypeText(subscriptionDetails?.subscription_period || '') }}
              </span>
            </div>
            <div class="flex justify-between items-center mb-2">
              <span class="text-white/60">Срок действия:</span>
              <span class="text-white font-medium">
                {{ formatDate(subscriptionDetails?.rent_start_date || '') }} - 
                {{ formatDate(subscriptionDetails?.rent_end_date || '') }}
              </span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-white/60">Статус:</span>
              <span class="text-sm" :class="{
                'text-green-400': subscriptionDetails?.status === 'PAID',
                'text-yellow-400': subscriptionDetails?.status === 'PENDING',
                'text-red-400': subscriptionDetails?.status === 'OVERDUE'
              }">
                {{ getStatusText(subscriptionDetails?.status || '') }}
              </span>
            </div>
          </div>

          <CustomButton
            v-if="!hasActiveSubscription"
            class="w-full"
            @click="navigateToSubscription"
          >
            Оформить подписку
          </CustomButton>
        </div>
      </div>

      <!-- Информация о поддержке -->
      <div class="text-center">
        <p class="text-white/60 text-sm">
          Если у вас возникли вопросы, обратитесь в поддержку:
          <a href="mailto:support@strelahack.local" class="text-primary hover:text-primary/80">
            support@strelahack.local
          </a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useFetch } from '~/composables/useFetch'
import { useToast } from 'primevue/usetoast'
import ProgressSpinner from 'primevue/progressspinner'
import CustomButton from '~/components/CustomButton.vue'

// Отключаем лейаут для этой страницы
definePageMeta({
  layout: false
})

const route = useRoute()
const { fetchWithAuth } = useFetch()
const toast = useToast()

const isLoading = ref(true)
const error = ref('')
const hasActiveSubscription = ref(false)
const subscriptionDetails = ref<Subscription | null>(null)

interface Subscription {
  id: number
  subscription_period: 'MONTH' | 'SEMESTER' | 'YEAR'
  rent_start_date: string
  rent_end_date: string
  status: 'PAID' | 'PENDING' | 'OVERDUE' | 'CANCELLED'
}

// Проверка статуса подписки
const checkSubscriptionStatus = async () => {
  try {
    // Имитация задержки запроса
    await new Promise(resolve => setTimeout(resolve, 1500))

    // Имитация данных
    const mockData = {
      has_active_subscription: true, // Всегда активна
      subscription_details: {
        id: 1,
        subscription_period: 'SEMESTER' as 'MONTH' | 'SEMESTER' | 'YEAR',
        rent_start_date: new Date().toISOString(),
        rent_end_date: new Date(Date.now() + 180 * 24 * 60 * 60 * 1000).toISOString(), // +180 дней (семестр)
        status: 'PAID' as 'PAID' | 'PENDING' | 'OVERDUE' | 'CANCELLED'
      }
    }

    hasActiveSubscription.value = mockData.has_active_subscription
    subscriptionDetails.value = mockData.subscription_details
  } catch (err) {
    error.value = 'Произошла ошибка при проверке статуса подписки'
    console.error('Ошибка проверки подписки:', err)
  } finally {
    isLoading.value = false
  }
}

// Форматирование даты
const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU')
}

// Получение текста типа подписки
const getSubscriptionTypeText = (period: string) => {
  switch (period) {
    case 'MONTH': return 'Месячная'
    case 'SEMESTER': return 'Семестровая'
    case 'YEAR': return 'Годовая'
    default: return period
  }
}

// Получение текста статуса
const getStatusText = (status: string) => {
  switch (status) {
    case 'PAID': return 'Оплачено'
    case 'PENDING': return 'Ожидает оплаты'
    case 'OVERDUE': return 'Просрочено'
    case 'CANCELLED': return 'Отменено'
    default: return status
  }
}

// Переход на страницу подписки
const navigateToSubscription = () => {
  window.location.href = '/profile'
}

onMounted(() => {
  checkSubscriptionStatus()
})
</script>

<style scoped>
.bg-custom-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
</style> 
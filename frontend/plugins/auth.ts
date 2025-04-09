import { useAuthStore } from '~/stores/auth'

export default defineNuxtPlugin(() => {
  const authStore = useAuthStore()
  
  // Инициализируем состояние авторизации при запуске приложения
  authStore.initializeAuth()
}) 
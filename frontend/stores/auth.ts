import { defineStore } from 'pinia'
import { useCookie } from '#app'

interface AuthState {
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean
}

interface RegisterData {
  firstName: string
  lastName: string
  birthDate: Date | null
  email: string
  password: string
  password2: string
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    accessToken: null,
    refreshToken: null,
    isAuthenticated: false
  }),

  actions: {
    async login(email: string, password: string) {
      try {
        const response = await fetch('/api/auth/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
        })

        const data = await response.json()

        if (response.ok) {
          // Сохраняем токены в cookies
          const accessCookie = useCookie('access_token', {
            maxAge: 7200, // 1 час
            secure: true,
            sameSite: 'strict'
          })
          const refreshCookie = useCookie('refresh_token', {
            maxAge: 14 * 24 * 3600, // 7 дней
            secure: true,
            sameSite: 'strict'
          })

          accessCookie.value = data.tokens.access
          refreshCookie.value = data.tokens.refresh

          // Обновляем состояние store
          this.accessToken = data.tokens.access
          this.refreshToken = data.tokens.refresh
          this.isAuthenticated = true

          return { success: true, message: data.message }
        } else {
          return { success: false, message: data.message || 'Ошибка авторизации' }
        }
      } catch (error) {
        console.error('Ошибка при авторизации:', error)
        return { success: false, message: 'Произошла ошибка при авторизации' }
      }
    },

    async register(data: RegisterData) {
      try {
        const response = await fetch('/api/auth/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        })

        const responseData = await response.json()

        if (response.ok) {
          // После успешной регистрации можно сразу авторизовать пользователя
          return this.login(data.email, data.password)
        } else {
          return { success: false, message: responseData.message || 'Ошибка при регистрации' }
        }
      } catch (error) {
        console.error('Ошибка при регистрации:', error)
        return { success: false, message: 'Произошла ошибка при регистрации' }
      }
    },

    logout() {
      // Удаляем cookies
      const accessCookie = useCookie('access_token')
      const refreshCookie = useCookie('refresh_token')
      
      accessCookie.value = null
      refreshCookie.value = null

      // Очищаем состояние store
      this.accessToken = null
      this.refreshToken = null
      this.isAuthenticated = false
    },

    // Инициализация состояния из cookies при загрузке приложения
    initializeAuth() {
      const accessCookie = useCookie('access_token')
      const refreshCookie = useCookie('refresh_token')

      if (accessCookie.value && refreshCookie.value) {
        this.accessToken = accessCookie.value
        this.refreshToken = refreshCookie.value
        this.isAuthenticated = true
      }
    }
  }
}) 
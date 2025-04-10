import { defineStore } from 'pinia'
import { useCookie } from '#app'

interface UserData {
  name: string
  surname: string
  fathername: string
  phone_number: string
  birth_date: string
  university: string
  faculty: string
  course: number
  email: string
  check_in_date: string
  check_out_date: string
  room: number
  is_admin: boolean
}

interface AuthState {
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  userData: UserData | null
}

interface LoginData {
  email: string
  password: string
  cfToken: string
}

interface RegisterData {
  firstName: string
  lastName: string
  birthDate: Date | null
  email: string
  password: string
  password2: string
  cfToken: string
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    accessToken: null,
    refreshToken: null,
    isAuthenticated: false,
    userData: null
  }),

  actions: {
    async login(email: string, password: string, cfToken: string) {
      try {
        const response = await fetch('/api/auth/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password, cf_token: cfToken })
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

          // Получаем данные пользователя после успешной авторизации
          await this.fetchUserData()

          return { success: true, message: data.message }
        } else {
          return { success: false, message: data.message || 'Ошибка авторизации' }
        }
      } catch (error) {
        console.error('Ошибка при авторизации:', error)
        return { success: false, message: 'Произошла ошибка при авторизации' }
      }
    },

    async fetchUserData(): Promise<{ success: boolean; data?: UserData; message?: string }> {
      try {
        const response = await fetch('/api/auth/profile/', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${this.accessToken}`,
            'Content-Type': 'application/json'
          }
        })

        if (response.ok) {
          const userData = await response.json()
          this.userData = userData
          return { success: true, data: userData }
        } else if (response.status === 401) {
          // Если токен истек, пробуем обновить его
          const refreshResponse = await fetch('/api/auth/token/refresh/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ refresh: this.refreshToken })
          })

          if (refreshResponse.ok) {
            const refreshData = await refreshResponse.json()
            
            // Обновляем токены в cookies
            const accessCookie = useCookie('access_token', {
              maxAge: 7200,
              secure: true,
              sameSite: 'strict'
            })
            accessCookie.value = refreshData.access
            
            // Обновляем токен в store
            this.accessToken = refreshData.access
            
            // Повторяем запрос данных пользователя
            return this.fetchUserData()
          } else {
            // Если не удалось обновить токен, разлогиниваем пользователя
            this.logout()
            return { success: false, message: 'Сессия истекла. Пожалуйста, войдите снова.' }
          }
        } else {
          throw new Error('Ошибка при получении данных пользователя')
        }
      } catch (error) {
        console.error('Ошибка при получении данных пользователя:', error)
        return { success: false, message: 'Не удалось получить данные пользователя' }
      }
    },

    async register(data: RegisterData) {
      try {
        const response = await fetch('/api/auth/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: data.email,
            password: data.password,
            password2: data.password2,
            cf_token: data.cfToken
          })
        })

        const responseData = await response.json()

        if (response.ok) {
          return this.login(data.email, data.password, data.cfToken)
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
      this.userData = null
    },

    // Инициализация состояния из cookies при загрузке приложения
    async initializeAuth() {
      const accessCookie = useCookie('access_token')
      const refreshCookie = useCookie('refresh_token')

      if (accessCookie.value && refreshCookie.value) {
        this.accessToken = accessCookie.value
        this.refreshToken = refreshCookie.value
        this.isAuthenticated = true
        
        // Получаем данные пользователя при инициализации
        await this.fetchUserData()
      }
    }
  }
}) 
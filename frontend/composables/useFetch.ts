import { useAuthStore } from '~/stores/auth'

export const useFetch = () => {
  const authStore = useAuthStore()

  const fetchWithAuth = async (url: string, options: RequestInit = {}) => {
    const token = authStore.accessToken
    
    if (!token) {
      throw new Error('Токен авторизации не найден')
    }
    
    const headers = {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...options.headers
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers
      })

      if (response.status === 401) {
        // Если токен истек, пробуем обновить его
        try {
          const refreshResponse = await fetch('/api/auth/token/refresh/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              refresh: authStore.refreshToken
            })
          })

          if (refreshResponse.ok) {
            const data = await refreshResponse.json()
            authStore.accessToken = data.access
            
            // Повторяем исходный запрос с новым токеном
            return fetchWithAuth(url, options)
          } else {
            // Если не удалось обновить токен, разлогиниваем пользователя
            authStore.logout()
            throw new Error('Сессия истекла. Пожалуйста, войдите снова.')
          }
        } catch (error) {
          authStore.logout()
          throw error
        }
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      return response
    } catch (error) {
      console.error('Ошибка при выполнении запроса:', error)
      throw error
    }
  }

  return {
    fetchWithAuth
  }
} 
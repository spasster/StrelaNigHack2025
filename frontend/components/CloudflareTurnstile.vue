<template>
  <div ref="container" class="cf-turnstile" :data-sitekey="siteKey"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  siteKey: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['verify'])
const container = ref(null)
let widgetId = null
let isInitialized = false

// Глобальная переменная для отслеживания загрузки скрипта
let scriptLoadingPromise = null

const loadTurnstileScript = () => {
  if (scriptLoadingPromise) {
    return scriptLoadingPromise
  }

  if (window.turnstile) {
    return Promise.resolve()
  }

  scriptLoadingPromise = new Promise((resolve) => {
    const script = document.createElement('script')
    script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js'
    script.async = true
    script.defer = true
    script.onload = () => {
      resolve()
    }
    document.head.appendChild(script)
  })

  return scriptLoadingPromise
}

onMounted(async () => {
  if (isInitialized) return
  
  try {
    // Загружаем скрипт Turnstile
    await loadTurnstileScript()

    // Ждем, пока контейнер будет доступен
    if (!container.value) return

    // Инициализируем Turnstile
    widgetId = window.turnstile?.render(container.value, {
      sitekey: props.siteKey,
      callback: (token) => {
        emit('verify', token)
      }
    })
    isInitialized = true
  } catch (error) {
    console.error('Ошибка при загрузке Turnstile:', error)
  }
})

onUnmounted(() => {
  if (widgetId) {
    window.turnstile?.reset(widgetId)
    widgetId = null
    isInitialized = false
  }
})
</script> 
<template>
  <Dialog
    v-model:visible="visible"
    modal
    :style="{ width: '450px' }"
    class="bg-custom-card border-none font-paratype"
  >
    <template #header>
      <h2 class="text-xl text-white font-semibold">Вход</h2>
    </template>

    <div class="flex flex-col gap-4">
      <div class="field">
        <span class="p-float-label">
          <InputText
            id="email"
            v-model="form.email"
            type="email"
            class="w-full"
          />
          <label class="text-white/50" for="email">Электронная почта</label>
        </span>
      </div>

      <div class="field">
        <span class="p-float-label">
          <Password
            id="password"
            v-model="form.password"
            :feedback="false"
            toggleMask
            class="w-full"
            input-class="w-full"
          />
          <label class="text-white/50" for="password">Пароль</label>
        </span>
      </div>

      <div class="field">
        <CloudflareTurnstile
          v-if="visible"
          :key="captchaKey"
          site-key="0x4AAAAAAAi8lBfwGM44vEO0"
          @verify="handleVerify"
        />
      </div>

      <div class="text-center text-sm">
        <span class="text-white/60">Нет аккаунта?</span>
        <a href="#" class="text-primary hover:text-primary/80 ml-1" @click.prevent="switchToRegistration">Зарегистрируйтесь</a>
      </div>
    </div>

    <template #footer>
      <CustomButton
        class="w-full"
        @click="handleSubmit"
      >Войти</CustomButton>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import { useToast } from 'primevue/usetoast'

const visible = ref(false)
const authStore = useAuthStore()
const toast = useToast()
const emit = defineEmits(['switch-to-registration'])
const captchaKey = ref(0)

// Показываем капчу только когда диалог видим
watch(visible, (newValue) => {
  if (newValue) {
    captchaKey.value++
  }
})

const form = reactive({
  email: '',
  password: '',
  cfToken: ''
})

const handleVerify = (token: string) => {
  form.cfToken = token
}

const handleSubmit = async () => {
  // Проверяем заполнение всех полей
  if (!form.email || !form.password) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Пожалуйста, заполните все поля',
      life: 3000
    })
    return
  }

  // Проверяем капчу
  if (!form.cfToken) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Пожалуйста, пройдите проверку капчи',
      life: 3000
    })
    return
  }

  try {
    const result = await authStore.login(form.email, form.password, form.cfToken)

    if (result.success) {
      toast.add({
        severity: 'success',
        summary: 'Успех',
        detail: 'Авторизация успешно завершена',
        life: 3000
      })
      visible.value = false
      // Очищаем форму
      form.email = ''
      form.password = ''
      form.cfToken = ''
    } else {
      toast.add({
        severity: 'error',
        summary: 'Ошибка',
        detail: result.message || 'Произошла ошибка при авторизации',
        life: 3000
      })
    }
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Произошла ошибка при авторизации',
      life: 3000
    })
  }
}

const switchToRegistration = () => {
  visible.value = false
  form.cfToken = ''
  emit('switch-to-registration')
}

// Экспортируем метод для открытия диалога
defineExpose({
  show: () => visible.value = true,
  hide: () => {
    visible.value = false
    form.cfToken = ''
  }
})
</script>

<style scoped>
:deep(.p-dialog) {
  @apply rounded-lg shadow-lg;
}

:deep(.p-dialog-header) {
  @apply pb-4;
}

:deep(.p-dialog-footer) {
  @apply pt-4;
}

:deep(.p-float-label) {
  @apply mb-2;
}
</style>
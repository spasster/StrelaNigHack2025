<template>
  <Dialog
    v-model:visible="visible"
    modal
    :style="{ width: '450px' }"
    class="bg-custom-card border-none font-paratype"
  >
    <template #header>
      <h2 class="text-xl text-white font-semibold">Регистрация</h2>
    </template>

    <div class="flex flex-col gap-4">
      <div class="field">
        <span class="p-float-label">
          <InputText
            id="firstName"
            v-model="form.firstName"
            class="w-full"
          />
          <label class="text-white/50" for="firstName">Имя как в паспорте</label>
        </span>
      </div>

      <div class="field">
        <span class="p-float-label">
          <InputText
            id="lastName"
            v-model="form.lastName"
            class="w-full"
          />
          <label class="text-white/50" for="lastName">Фамилия как в паспорте</label>
        </span>
      </div>

      <div class="field">
        <span class="p-float-label">
          <Calendar
            id="birthDate"
            v-model="form.birthDate"
            class="w-full"
            dateFormat="dd/mm/yy"
          />
          <label class="text-white/50" for="birthDate">Дата рождения</label>
        </span>
      </div>

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
        <span class="p-float-label">
          <Password
            id="password2"
            v-model="form.password2"
            :feedback="false"
            toggleMask
            class="w-full"
            input-class="w-full"
          />
          <label class="text-white/50" for="password2">Повторите пароль</label>
        </span>
      </div>

      <div class="text-center text-sm">
        <span class="text-white/60">Уже есть аккаунт?</span>
        <a href="#" class="text-primary hover:text-primary/80 ml-1" @click.prevent="switchToLogin">Войдите</a>
      </div>
    </div>

    <template #footer>
      <CustomButton
        class="w-full"
        @click="handleSubmit"
      >Сохранить и продолжить</CustomButton>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import { useToast } from 'primevue/usetoast'

const visible = ref(false)
const authStore = useAuthStore()
const toast = useToast()
const emit = defineEmits(['switch-to-login'])

const form = reactive({
  firstName: '',
  lastName: '',
  birthDate: null,
  email: '',
  password: '',
  password2: ''
})

const switchToLogin = () => {
  visible.value = false
  emit('switch-to-login')
}

const handleSubmit = async () => {
  // Проверяем заполнение всех полей
  if (!form.firstName || !form.lastName || !form.birthDate || !form.email || !form.password || !form.password2) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Пожалуйста, заполните все поля',
      life: 3000
    })
    return
  }

  // Проверяем совпадение паролей
  if (form.password !== form.password2) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Пароли не совпадают',
      life: 3000
    })
    return
  }

  try {
    const result = await authStore.register({
      firstName: form.firstName,
      lastName: form.lastName,
      birthDate: form.birthDate,
      email: form.email,
      password: form.password,
      password2: form.password2
    })

    if (result.success) {
      toast.add({
        severity: 'success',
        summary: 'Успех',
        detail: 'Регистрация успешно завершена',
        life: 3000
      })
      visible.value = false
      // Очищаем форму
      form.firstName = ''
      form.lastName = ''
      form.birthDate = null
      form.email = ''
      form.password = ''
      form.password2 = ''
    } else {
      toast.add({
        severity: 'error',
        summary: 'Ошибка',
        detail: result.message || 'Произошла ошибка при регистрации',
        life: 3000
      })
    }
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Произошла ошибка при регистрации',
      life: 3000
    })
  }
}

// Экспортируем метод для открытия диалога
defineExpose({
  show: () => visible.value = true,
  hide: () => visible.value = false
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
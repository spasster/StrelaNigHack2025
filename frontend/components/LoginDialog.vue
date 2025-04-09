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

const form = reactive({
  email: '',
  password: ''
})

const switchToRegistration = () => {
  visible.value = false
  emit('switch-to-registration')
}

const handleSubmit = async () => {
  const result = await authStore.login(form.email, form.password)
  
  if (result.success) {
    toast.add({
      severity: 'success',
      summary: 'Успех',
      detail: result.message,
      life: 3000
    })
    visible.value = false
    // Очищаем форму
    form.email = ''
    form.password = ''
  } else {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: result.message,
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
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
const visible = ref(false)
const form = reactive({
  email: '',
  password: ''
})

const handleSubmit = () => {
  // Здесь будет логика отправки формы
  console.log('Form submitted:', form)
}

// Экспортируем метод для открытия диалога
defineExpose({
  show: () => visible.value = true
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
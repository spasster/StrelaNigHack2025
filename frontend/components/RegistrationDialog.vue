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

const visible = ref(false)
const form = reactive({
  firstName: '',
  lastName: '',
  birthDate: null,
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
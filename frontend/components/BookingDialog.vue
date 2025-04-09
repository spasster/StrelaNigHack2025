<!-- components/BookingDialog.vue -->
<template>
  <Dialog
    v-model:visible="visible"
    modal
    :style="{ width: '450px' }"
    class="bg-custom-card border-none font-paratype"
  >
    <template #header>
      <h2 class="text-xl text-white font-semibold">Бронирование номера</h2>
    </template>

    <div class="flex flex-col gap-4">
      <div class="field">
        <span class="p-float-label">
          <InputText
            v-model="form.name"
            class="w-full"
          />
          <label class="text-white/50">Имя</label>
        </span>
        <small v-if="errors.name" class="text-red-400">{{ errors.name }}</small>
      </div>

      <div class="field">
        <span class="p-float-label">
          <InputText
            v-model="form.surname"
            class="w-full"
          />
          <label class="text-white/50">Фамилия</label>
        </span>
        <small v-if="errors.surname" class="text-red-400">{{ errors.surname }}</small>
      </div>

      <div class="field">
        <span class="p-float-label">
          <InputText
            v-model="form.fathername"
            class="w-full"
          />
          <label class="text-white/50">Отчество</label>
        </span>
        <small v-if="errors.fathername" class="text-red-400">{{ errors.fathername }}</small>
      </div>

      <div class="field">
        <span class="p-float-label">
          <InputText
            v-model="form.phone_number"
            class="w-full"
            placeholder="+7 (999) 999-99-99"
          />
          <label class="text-white/50">Номер телефона</label>
        </span>
        <small v-if="errors.phone_number" class="text-red-400">{{ errors.phone_number }}</small>
      </div>

      <div class="field">
        <span class="p-float-label">
          <Calendar
            v-model="form.birth_date"
            dateFormat="yy-mm-dd"
            :maxDate="new Date()"
            class="w-full"
          />
          <label class="text-white/50">Дата рождения</label>
        </span>
        <small v-if="errors.birth_date" class="text-red-400">{{ errors.birth_date }}</small>
      </div>

      <div class="field">
        <span class="p-float-label">
          <InputText
            v-model="form.university"
            class="w-full"
          />
          <label class="text-white/50">Университет</label>
        </span>
        <small v-if="errors.university" class="text-red-400">{{ errors.university }}</small>
      </div>

      <div class="field">
        <span class="p-float-label">
          <InputText
            v-model="form.faculty"
            class="w-full"
          />
          <label class="text-white/50">Факультет</label>
        </span>
        <small v-if="errors.faculty" class="text-red-400">{{ errors.faculty }}</small>
      </div>

      <div class="field">
        <span class="p-float-label">
          <InputNumber
            v-model="form.course"
            :min="1"
            :max="6"
            class="w-full"
          />
          <label class="text-white/50">Курс</label>
        </span>
        <small v-if="errors.course" class="text-red-400">{{ errors.course }}</small>
      </div>

      <div class="field">
        <span class="p-float-label">
          <InputText
            v-model="form.email"
            type="email"
            class="w-full"
          />
          <label class="text-white/50">Email</label>
        </span>
        <small v-if="errors.email" class="text-red-400">{{ errors.email }}</small>
      </div>

      <div class="field">
        <span class="p-float-label">
          <Calendar
            v-model="form.check_in_date"
            dateFormat="yy-mm-dd"
            :minDate="new Date()"
            class="w-full"
          />
          <label class="text-white/50">Дата заселения</label>
        </span>
        <small v-if="errors.check_in_date" class="text-red-400">{{ errors.check_in_date }}</small>
      </div>

      <div class="field">
        <span class="p-float-label">
          <Calendar
            v-model="form.check_out_date"
            dateFormat="yy-mm-dd"
            :minDate="form.check_in_date || new Date()"
            class="w-full"
          />
          <label class="text-white/50">Дата выселения</label>
        </span>
        <small v-if="errors.check_out_date" class="text-red-400">{{ errors.check_out_date }}</small>
      </div>
    </div>

    <template #footer>
      <CustomButton
        class="w-full"
        @click="handleSubmit"
      >Забронировать</CustomButton>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { useToast } from 'primevue/usetoast'

const props = defineProps<{
  roomId: number
}>()

const emit = defineEmits(['success'])
const visible = ref(false)
const toast = useToast()

const form = reactive({
  name: '',
  surname: '',
  fathername: '',
  phone_number: '',
  birth_date: null as Date | null,
  university: '',
  faculty: '',
  course: null as number | null,
  email: '',
  check_in_date: null as Date | null,
  check_out_date: null as Date | null
})

const errors = reactive({
  name: '',
  surname: '',
  fathername: '',
  phone_number: '',
  birth_date: '',
  university: '',
  faculty: '',
  course: '',
  email: '',
  check_in_date: '',
  check_out_date: ''
})

const clearErrors = () => {
  Object.keys(errors).forEach(key => {
    errors[key as keyof typeof errors] = ''
  })
}

const handleSubmit = async () => {
  clearErrors()
  
  if (!props.roomId) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Номер не выбран',
      life: 3000
    })
    return
  }

  // Проверяем заполнение всех полей
  const requiredFields = ['name', 'surname', 'fathername', 'phone_number', 'birth_date', 
                         'university', 'faculty', 'course', 'email', 'check_in_date', 'check_out_date']
  
  const emptyFields = requiredFields.filter(field => {
    const value = form[field as keyof typeof form]
    return value === null || value === '' || value === undefined
  })

  if (emptyFields.length > 0) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Заполните все поля',
      life: 3000
    })
    return
  }

  try {
    const response = await fetch('/api/rooms/check-in/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        room: props.roomId,
        name: form.name,
        surname: form.surname,
        fathername: form.fathername,
        phone_number: form.phone_number,
        birth_date: form.birth_date?.toISOString().split('T')[0],
        university: form.university,
        faculty: form.faculty,
        course: form.course,
        email: form.email,
        check_in_date: form.check_in_date?.toISOString(),
        check_out_date: form.check_out_date?.toISOString()
      }),
    })

    if (response.ok) {
      toast.add({
        severity: 'success',
        summary: 'Успех',
        detail: 'Номер успешно забронирован',
        life: 3000
      })
      visible.value = false
      emit('success')
    } else {
      const data = await response.json()
      Object.keys(data).forEach(key => {
        if (key in errors) {
          errors[key as keyof typeof errors] = data[key]
        }
      })
    }
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось забронировать номер',
      life: 3000
    })
  }
}

defineExpose({
  showDialog: () => visible.value = true,
  hideDialog: () => visible.value = false
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

:deep(.p-calendar) {
  @apply w-full;
}

:deep(.p-inputtext) {
  @apply w-full;
}

:deep(.p-inputnumber) {
  @apply w-full;
}
</style> 
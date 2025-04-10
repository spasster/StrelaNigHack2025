<template>
  <div class="p-4">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-white/85">Управление заселением</h2>
      <Button label="Новое заселение" icon="pi pi-user-plus" class="p-button-primary" @click="showCheckInDialog = true" />
    </div>

    <Card class="mb-4">
      <template #content>
        <DataTable :value="checkIns" :paginator="true" :rows="10" 
                   class="p-datatable-sm" stripedRows
                   :globalFilterFields="['id', 'room', 'name', 'surname', 'university', 'check_in_date']"
                   v-model:filters="filters"
                   :loading="loading"
                   loadingIcon="pi pi-spinner pi-spin">
          <template #empty>
            <div class="flex flex-col items-center justify-center p-4">
              <i class="pi pi-inbox text-4xl text-white/50 mb-2"></i>
              <span class="text-white/50">Нет данных для отображения</span>
            </div>
          </template>
          <template #loading>
            <div class="flex items-center justify-center p-4">
              <i class="pi pi-spinner pi-spin text-2xl text-white/50 mr-2"></i>
              <span class="text-white/50">Загрузка...</span>
            </div>
          </template>
          <template #header>
            <div class="flex justify-end">
              <span class="p-input-icon-left">
                <i class="pi pi-search ml-2" />
                <InputText v-model="filters['global'].value" placeholder="Поиск..." class="ml-4" />
              </span>
            </div>
          </template>
          <Column field="id" header="ID" sortable></Column>
          <Column field="room" header="Комната" sortable></Column>
          <Column field="name" header="Имя" sortable></Column>
          <Column field="surname" header="Фамилия" sortable></Column>
          <Column field="university" header="Университет" sortable></Column>
          <Column field="check_in_date" header="Дата заселения" sortable>
            <template #body="{ data }">
              <Tag :value="new Date(data.check_in_date).toLocaleDateString()" severity="info" />
            </template>
          </Column>
          <Column header="Действия" style="width: 100px">
            <template #body="{ data }">
              <div class="flex gap-2">
                <Button icon="pi pi-pencil" class="p-button-rounded p-button-text" @click="editCheckIn(data)" />
                <Button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger" @click="confirmDeleteCheckIn(data)" />
              </div>
            </template>
          </Column>
        </DataTable>
      </template>
    </Card>

    <!-- Диалог создания/редактирования заселения -->
    <Dialog v-model:visible="showCheckInDialog" 
            :header="editingCheckIn ? 'Редактирование заселения' : 'Новое заселение'" 
            :style="{ width: '700px' }" :modal="true" 
            class="bg-custom-card border-none font-paratype">
      <div class="grid grid-cols-2 gap-6">
        <div class="field">
          <span class="p-float-label">
            <Dropdown 
              id="room" 
              v-model="checkInForm.room" 
              :options="availableRooms" 
              optionLabel="name"
              optionValue="id"
              placeholder="Выберите комнату"
              class="w-full"
              :filter="true"
              filterPlaceholder="Поиск комнаты"
              :showClear="true"
            />
            <label class="text-white/50" for="room">Комната</label>
          </span>
        </div>
        <div class="field">
          <span class="p-float-label">
            <InputText id="name" v-model="checkInForm.name" class="w-full" />
            <label class="text-white/50" for="name">Имя</label>
          </span>
        </div>
        <div class="field">
          <span class="p-float-label">
            <InputText id="surname" v-model="checkInForm.surname" class="w-full" />
            <label class="text-white/50" for="surname">Фамилия</label>
          </span>
        </div>
        <div class="field">
          <span class="p-float-label">
            <InputText id="fathername" v-model="checkInForm.fathername" class="w-full" />
            <label class="text-white/50" for="fathername">Отчество</label>
          </span>
        </div>
        <div class="field">
          <span class="p-float-label">
            <InputText id="phone" v-model="checkInForm.phone_number" class="w-full" />
            <label class="text-white/50" for="phone">Телефон</label>
          </span>
        </div>
        <div class="field">
          <span class="p-float-label">
            <Calendar id="birth_date" v-model="checkInForm.birth_date" dateFormat="dd.mm.yy" class="w-full" />
            <label class="text-white/50" for="birth_date">Дата рождения</label>
          </span>
        </div>
        <div class="field">
          <span class="p-float-label">
            <InputText id="university" v-model="checkInForm.university" class="w-full" />
            <label class="text-white/50" for="university">Университет</label>
          </span>
        </div>
        <div class="field">
          <span class="p-float-label">
            <InputText id="faculty" v-model="checkInForm.faculty" class="w-full" />
            <label class="text-white/50" for="faculty">Факультет</label>
          </span>
        </div>
        <div class="field">
          <span class="p-float-label">
            <InputNumber id="course" v-model="checkInForm.course" :min="1" :max="6" class="w-full" />
            <label class="text-white/50" for="course">Курс</label>
          </span>
        </div>
        <div class="field">
          <span class="p-float-label">
            <InputText id="email" v-model="checkInForm.email" type="email" class="w-full" />
            <label class="text-white/50" for="email">Email</label>
          </span>
        </div>
        <div class="field">
          <span class="p-float-label">
            <Calendar id="check_in_date" v-model="checkInForm.check_in_date" dateFormat="dd.mm.yy" showTime class="w-full" />
            <label class="text-white/50" for="check_in_date">Дата заселения</label>
          </span>
        </div>
        <div class="field">
          <span class="p-float-label">
            <Calendar id="check_out_date" v-model="checkInForm.check_out_date" dateFormat="dd.mm.yy" showTime class="w-full" />
            <label class="text-white/50" for="check_out_date">Дата выселения</label>
          </span>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button label="Отмена" icon="pi pi-times" class="p-button-text" @click="closeCheckInDialog" />
          <Button :label="editingCheckIn ? 'Сохранить' : 'Создать'" icon="pi pi-check" class="p-button-primary" @click="saveCheckIn" />
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useFetch } from '~/composables/useFetch'
import { useToast } from 'primevue/usetoast'

const toast = useToast()
const { fetchWithAuth } = useFetch()
const loading = ref(false)
const checkIns = ref([])
const availableRooms = ref([])
const showCheckInDialog = ref(false)
const editingCheckIn = ref(null)

const filters = ref({
  global: { value: null, matchMode: 'contains' }
})

const checkInForm = ref({
  name: '',
  surname: '',
  fathername: '',
  phone_number: '',
  birth_date: null,
  university: '',
  faculty: '',
  course: 1,
  email: '',
  check_in_date: null,
  check_out_date: null,
  room: null
})

const formatDate = (date) => {
  if (!date) return null
  const d = new Date(date)
  return d.toISOString().split('T')[0]
}

const loadCheckIns = async () => {
  loading.value = true
  try {
    const response = await fetchWithAuth('/api/rooms/check-in/all/')
    const data = await response.json()
    checkIns.value = data
  } catch (error) {
    console.error('Ошибка при загрузке заселений:', error)
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось загрузить список заселений',
      life: 3000
    })
  } finally {
    loading.value = false
  }
}

const loadAvailableRooms = async () => {
  try {
    const response = await fetchWithAuth('/api/rooms/list/')
    const data = await response.json()
    // Добавляем поле name для отображения в выпадающем списке
    availableRooms.value = data.map(room => ({
      ...room,
      name: `Комната ${room.id} (${room.type})`
    }))
  } catch (error) {
    console.error('Ошибка при загрузке комнат:', error)
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось загрузить список комнат',
      life: 3000
    })
  }
}

const createCheckIn = async () => {
  try {
    // Создаем заселение с комнатой
    const checkInResponse = await fetchWithAuth('/api/rooms/check-in/', {
      method: 'POST',
      body: JSON.stringify({
        name: checkInForm.value.name,
        surname: checkInForm.value.surname,
        fathername: checkInForm.value.fathername,
        phone_number: checkInForm.value.phone_number,
        birth_date: formatDate(checkInForm.value.birth_date),
        university: checkInForm.value.university,
        faculty: checkInForm.value.faculty,
        course: checkInForm.value.course,
        email: checkInForm.value.email,
        check_in_date: formatDate(checkInForm.value.check_in_date),
        check_out_date: formatDate(checkInForm.value.check_out_date),
        room: checkInForm.value.room
      })
    })

    const checkInData = await checkInResponse.json()

    // Если комната не указана, отвязываем её
    if (!checkInForm.value.room) {
      await fetchWithAuth('/api/rooms/check-in/unassign/', {
        method: 'POST',
        body: JSON.stringify({
          check_in_id: checkInData.id
        })
      })
    }

    toast.add({
      severity: 'success',
      summary: 'Успешно',
      detail: 'Заселение создано',
      life: 3000
    })
    closeCheckInDialog()
    loadCheckIns()
  } catch (error) {
    console.error('Ошибка при создании заселения:', error)
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось создать заселение',
      life: 3000
    })
  }
}

const updateCheckIn = async () => {
  try {
    const checkInId = checkInForm.value.id

    // Обновляем данные заселения
    await fetchWithAuth(`/api/rooms/check-in/${checkInId}/`, {
      method: 'PUT',
      body: JSON.stringify({
        name: checkInForm.value.name,
        surname: checkInForm.value.surname,
        fathername: checkInForm.value.fathername,
        phone_number: checkInForm.value.phone_number,
        birth_date: formatDate(checkInForm.value.birth_date),
        university: checkInForm.value.university,
        faculty: checkInForm.value.faculty,
        course: checkInForm.value.course,
        email: checkInForm.value.email,
        check_in_date: formatDate(checkInForm.value.check_in_date),
        check_out_date: formatDate(checkInForm.value.check_out_date)
      })
    })

    // Если изменилась комната
    if (checkInForm.value.room !== checkInForm.value.old_room) {
      // Если была старая комната, отвязываем от неё
      if (checkInForm.value.old_room) {
        await fetchWithAuth('/api/rooms/check-in/unassign/', {
          method: 'POST',
          body: JSON.stringify({
            check_in_id: checkInId
          })
        })
      }

      // Если указана новая комната, назначаем её
      if (checkInForm.value.room) {
        await fetchWithAuth('/api/rooms/check-in/assign/', {
          method: 'POST',
          body: JSON.stringify({
            check_in_id: checkInId,
            room_id: checkInForm.value.room
          })
        })
      }
    }

    toast.add({
      severity: 'success',
      summary: 'Успешно',
      detail: 'Заселение обновлено',
      life: 3000
    })
    closeCheckInDialog()
    loadCheckIns()
  } catch (error) {
    console.error('Ошибка при обновлении заселения:', error)
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось обновить заселение',
      life: 3000
    })
  }
}

const saveCheckIn = async () => {
  try {
    if (editingCheckIn.value) {
      await updateCheckIn()
    } else {
      await createCheckIn()
    }
  } catch (error) {
    console.error('Ошибка при сохранении заселения:', error)
  }
}

const confirmDeleteCheckIn = (checkIn) => {
  if (confirm('Вы уверены, что хотите удалить это заселение?')) {
    deleteCheckIn(checkIn.id)
  }
}

const deleteCheckIn = async (id) => {
  try {
    // Сначала отвязываем от комнаты, если есть
    await fetchWithAuth('/api/rooms/check-in/unassign/', {
      method: 'POST',
      body: JSON.stringify({
        check_in_id: id
      })
    })

    // Затем удаляем заселение
    await fetchWithAuth(`/api/rooms/check-in/${id}/`, {
      method: 'DELETE'
    })

    toast.add({
      severity: 'success',
      summary: 'Успешно',
      detail: 'Заселение удалено',
      life: 3000
    })
    loadCheckIns()
  } catch (error) {
    console.error('Ошибка при удалении заселения:', error)
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось удалить заселение',
      life: 3000
    })
  }
}

const editCheckIn = (checkIn) => {
  editingCheckIn.value = checkIn
  checkInForm.value = { 
    ...checkIn,
    birth_date: checkIn.birth_date ? new Date(checkIn.birth_date) : null,
    check_in_date: checkIn.check_in_date ? new Date(checkIn.check_in_date) : null,
    check_out_date: checkIn.check_out_date ? new Date(checkIn.check_out_date) : null
  }
  showCheckInDialog.value = true
}

const closeCheckInDialog = () => {
  showCheckInDialog.value = false
  editingCheckIn.value = null
  checkInForm.value = {
    name: '',
    surname: '',
    fathername: '',
    phone_number: '',
    birth_date: null,
    university: '',
    faculty: '',
    course: 1,
    email: '',
    check_in_date: null,
    check_out_date: null,
    room: null
  }
}

onMounted(() => {
  loadCheckIns()
  loadAvailableRooms()
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
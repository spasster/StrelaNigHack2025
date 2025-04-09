<template>
  <div class="p-4">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-white/85">Управление комнатами</h2>
      <Button label="Создать комнату" icon="pi pi-plus" class="p-button-primary" @click="showCreateRoomDialog = true" />
    </div>

    <Card class="mb-4">
      <template #content>
        <DataTable :value="rooms" :paginator="true" :rows="10" 
                   class="p-datatable-sm" stripedRows
                   :globalFilterFields="['id', 'seats', 'occupied_seats', 'gender']"
                   v-model:filters="filters"
                   :loading="loading"
                   loadingIcon="pi pi-spinner pi-spin">
          <template #header>
            <div class="flex justify-end">
              <span class="p-input-icon-left">
                <i class="pi pi-search ml-2" />
                <InputText v-model="filters['global'].value" placeholder="Поиск..." class="ml-4" />
              </span>
            </div>
          </template>
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
          <Column field="id" header="ID" sortable></Column>
          <Column field="seats" header="Мест" sortable></Column>
          <Column field="occupied_seats" header="Занято" sortable></Column>
          <Column field="gender" header="Пол" sortable>
            <template #body="{ data }">
              <Tag :value="data.gender === 'M' ? 'Мужской' : 'Женский'" 
                   :severity="data.gender === 'M' ? 'info' : 'warning'" />
            </template>
          </Column>
          <Column header="Действия">
            <template #body="{ data }">
              <div class="flex gap-2">
                <Button icon="pi pi-pencil" class="p-button-rounded p-button-text" @click="editRoom(data)" />
                <Button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger" @click="confirmDeleteRoom(data)" />
                <Button icon="pi pi-list" class="p-button-rounded p-button-text p-button-success" @click="showRoomDetails(data)" />
              </div>
            </template>
          </Column>
        </DataTable>
      </template>
    </Card>

    <!-- Диалог создания/редактирования комнаты -->
    <Dialog v-model:visible="showCreateRoomDialog" 
            :header="editingRoom ? 'Редактирование комнаты' : 'Создание комнаты'" 
            :style="{ width: '450px' }" :modal="true" 
            class="bg-custom-card border-none font-paratype">
      <div class="field">
        <span class="p-float-label">
          <InputNumber id="number" v-model="roomForm.number" :min="100" :max="399" :step="1" class="w-full" />
          <label class="text-white/50" for="number">Номер комнаты</label>
        </span>
      </div>
      <div class="field mt-4">
        <span class="p-float-label">
          <InputNumber id="seats" v-model="roomForm.seats" :min="1" class="w-full" />
          <label class="text-white/50" for="seats">Количество мест</label>
        </span>
      </div>
      <div class="field mt-4">
        <span class="p-float-label">
          <SelectButton id="gender" v-model="roomForm.gender" :options="genderOptions" 
                       optionLabel="label" optionValue="value" class="w-full" />
          <label class="text-white/50" for="gender">Пол</label>
        </span>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button label="Отмена" icon="pi pi-times" class="p-button-text" @click="closeRoomDialog" />
          <Button :label="editingRoom ? 'Сохранить' : 'Создать'" icon="pi pi-check" class="p-button-primary" @click="saveRoom" />
        </div>
      </template>
    </Dialog>

    <!-- Диалог деталей комнаты -->
    <Dialog v-model:visible="showRoomDetailsDialog" header="Детали комнаты" 
            :style="{ width: '700px' }" :modal="true" 
            class="bg-custom-card border-none font-paratype">
      <div v-if="selectedRoom" class="space-y-6">
        <!-- Информация о комнате -->
        <div class="bg-white/10 p-6 rounded-lg">
          <h3 class="text-lg font-semibold text-white/85 mb-4">Информация о комнате</h3>
          <div class="grid grid-cols-2 gap-6">
            <div class="flex items-center gap-3 p-3 bg-white/5 rounded-lg">
              <i class="pi pi-id-card text-white/50 text-xl"></i>
              <div>
                <span class="text-sm text-white/50 block">ID комнаты</span>
                <span class="font-medium text-white/85">{{ selectedRoom.id }}</span>
              </div>
            </div>
            <div class="flex items-center gap-3 p-3 bg-white/5 rounded-lg">
              <i class="pi pi-users text-white/50 text-xl"></i>
              <div>
                <span class="text-sm text-white/50 block">Количество мест</span>
                <span class="font-medium text-white/85">{{ selectedRoom.seats }}</span>
              </div>
            </div>
            <div class="flex items-center gap-3 p-3 bg-white/5 rounded-lg">
              <i class="pi pi-user text-white/50 text-xl"></i>
              <div>
                <span class="text-sm text-white/50 block">Занято мест</span>
                <span class="font-medium text-white/85">{{ selectedRoom.occupied_seats }}</span>
              </div>
            </div>
            <div class="flex items-center gap-3 p-3 bg-white/5 rounded-lg">
              <i class="pi pi-info-circle text-white/50 text-xl"></i>
              <div>
                <span class="text-sm text-white/50 block">Пол</span>
                <Tag :value="selectedRoom.gender === 'M' ? 'Мужской' : 'Женский'" 
                     :severity="selectedRoom.gender === 'M' ? 'info' : 'warning'" />
              </div>
            </div>
          </div>
        </div>

        <!-- Мебель -->
        <div class="bg-white/10 p-6 rounded-lg">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-semibold text-white/85">Мебель</h3>
            <div class="flex gap-2">
              <InputText v-model="furnitureForm.type" placeholder="Тип мебели" class="w-40" />
              <InputNumber v-model="furnitureForm.count" :min="1" :max="10" placeholder="Кол-во" class="w-24" />
              <Button label="Добавить" icon="pi pi-plus" class="p-button-primary" @click="addFurniture" />
            </div>
          </div>
          <DataTable :value="selectedRoom.furniture" :paginator="true" :rows="5" 
                     class="p-datatable-sm" stripedRows
                     :globalFilterFields="['type']"
                     v-model:filters="furnitureFilters"
                     :loading="furnitureLoading"
                     loadingIcon="pi pi-spinner pi-spin">
            <template #header>
              <div class="flex justify-end">
                <span class="p-input-icon-left">
                  <i class="pi pi-search ml-2" />
                  <InputText v-model="furnitureFilters['global'].value" placeholder="Поиск..." class="ml-4" />
                </span>
              </div>
            </template>
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
            <Column field="type" header="Тип"></Column>
            <Column field="count" header="Количество"></Column>
            <Column header="Действия" style="width: 100px">
              <template #body="{ data }">
                <Button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger" @click="deleteFurniture(data)" />
              </template>
            </Column>
          </DataTable>
        </div>
      </div>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'

const toast = useToast()
const rooms = ref([])
const showCreateRoomDialog = ref(false)
const showRoomDetailsDialog = ref(false)
const selectedRoom = ref(null)
const editingRoom = ref(null)
const furnitureForm = ref({
  type: '',
  count: 1
})
const loading = ref(false)
const furnitureLoading = ref(false)

const filters = ref({
  global: { value: null, matchMode: 'contains' }
})

const furnitureFilters = ref({
  global: { value: null, matchMode: 'contains' }
})

const roomForm = ref({
  number: null,
  seats: 1,
  gender: 'M'
})

const genderOptions = [
  { label: 'Мужской', value: 'M' },
  { label: 'Женский', value: 'F' }
]

// Загрузка списка комнат
const loadRooms = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/rooms/list/')
    rooms.value = await response.json()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Ошибка', detail: 'Не удалось загрузить список комнат', life: 3000 })
  } finally {
    loading.value = false
  }
}

// Создание/редактирование комнаты
const saveRoom = async () => {
  try {
    const url = editingRoom.value 
      ? `/api/rooms/${editingRoom.value.id}/` 
      : '/api/rooms/create/'
    const method = editingRoom.value ? 'PUT' : 'POST'

    // Сначала сохраняем комнату
    const roomResponse = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        number: roomForm.value.number,
        seats: roomForm.value.seats,
        gender: roomForm.value.gender
      })
    })

    if (!roomResponse.ok) {
      throw new Error('Ошибка при сохранении комнаты')
    }

    const roomData = await roomResponse.json()

    // Затем сохраняем мебель
    if (furnitureForm.value.count > 0) {
      const furniturePromises = Array.from({ length: furnitureForm.value.count }, () => 
        fetch('/api/rooms/furniture/create/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            type: furnitureForm.value.type,
            room: roomData.id
          })
        })
      )

      await Promise.all(furniturePromises)
    }

    toast.add({
      severity: 'success',
      summary: 'Успешно',
      detail: 'Комната сохранена',
      life: 3000
    })
    closeRoomDialog()
    loadRooms()
  } catch (error) {
    console.error('Ошибка при сохранении комнаты:', error)
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось сохранить комнату',
      life: 3000
    })
  }
}

// Удаление комнаты
const confirmDeleteRoom = (room) => {
  if (confirm('Вы уверены, что хотите удалить эту комнату?')) {
    deleteRoom(room)
  }
}

const deleteRoom = async (room) => {
  try {
    const response = await fetch(`/api/rooms/${room.id}/`, { method: 'DELETE' })
    if (response.ok) {
      toast.add({ severity: 'success', summary: 'Успех', detail: 'Комната удалена', life: 3000 })
      loadRooms()
    }
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Ошибка', detail: 'Не удалось удалить комнату', life: 3000 })
  }
}

// Управление мебелью
const addFurniture = async () => {
  if (!selectedRoom.value) return

  if (!furnitureForm.value.type || !furnitureForm.value.count) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Заполните все поля',
      life: 3000
    })
    return
  }

  try {
    const response = await fetch('/api/rooms/furniture/create/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        type: furnitureForm.value.type,
        count: furnitureForm.value.count,
        condition: 'good',
        room: selectedRoom.value.id
      })
    })

    if (!response.ok) {
      throw new Error('Ошибка при сохранении мебели')
    }

    const result = await response.json()
    
    if (!selectedRoom.value.furniture) {
      selectedRoom.value.furniture = []
    }
    
    // Добавляем новую мебель в список
    selectedRoom.value.furniture.push({
      id: result.data.id,
      type: result.data.type,
      count: furnitureForm.value.count,
      condition: 'good'
    })
    
    // Очищаем форму
    furnitureForm.value = {
      type: '',
      count: 1
    }

    toast.add({
      severity: 'success',
      summary: 'Успешно',
      detail: result.message,
      life: 3000
    })
  } catch (error) {
    console.error('Ошибка при добавлении мебели:', error)
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось добавить мебель',
      life: 3000
    })
  }
}

const deleteFurniture = async (furniture) => {
  try {
    const response = await fetch(`/api/rooms/furniture/${furniture.id}/delete/`, { method: 'DELETE' })
    if (response.ok) {
      toast.add({ severity: 'success', summary: 'Успех', detail: 'Мебель удалена', life: 3000 })
      loadRoomDetails(selectedRoom.value.id)
    }
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Ошибка', detail: 'Не удалось удалить мебель', life: 3000 })
  }
}

// Вспомогательные методы
const editRoom = (room) => {
  editingRoom.value = room
  roomForm.value = { ...room }
  showCreateRoomDialog.value = true
}

const showRoomDetails = async (room) => {
  selectedRoom.value = room
  await loadRoomDetails(room.id)
  showRoomDetailsDialog.value = true
}

const loadRoomDetails = async (roomId) => {
  furnitureLoading.value = true
  try {
    const response = await fetch(`/api/rooms/detail/${roomId}/`)
    selectedRoom.value = await response.json()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Ошибка', detail: 'Не удалось загрузить детали комнаты', life: 3000 })
  } finally {
    furnitureLoading.value = false
  }
}

const closeRoomDialog = () => {
  showCreateRoomDialog.value = false
  editingRoom.value = null
  roomForm.value = {
    number: null,
    seats: 1,
    gender: 'M'
  }
}

onMounted(() => {
  loadRooms()
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
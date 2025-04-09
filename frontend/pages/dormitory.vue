<!-- pages/dormitory.vue -->
<script setup>
const dormData = ref({
  buildings: [
    {
      id: 1,
      name: 'Корпус А',
      floors: [
        {
          number: 5,
          rooms: [
            { 
              id: 501, 
              status: 'free', 
              capacity: 2,
              furniture: [
                { name: 'Кровать', count: 2 },
                { name: 'Шкаф', count: 2 }
              ],
              residents: []
            }
          ]
        }
      ]
    }
  ]
})

const selectedBuilding = ref(null)
const selectedFloor = ref(null)
const selectedRoom = ref(null)
const newResident = reactive({
  name: '',
  moveInDate: null,
  contact: ''
})
const newFurniture = reactive({
  name: '',
  count: 1
})

const showRoomDialog = ref(false)
const showResidentDialog = ref(false)

// Вычисляемые свойства
const availableFloors = computed(() => {
  if (!selectedBuilding.value) return []
  return dormData.value.buildings.find(b => b.id === selectedBuilding.value)?.floors || []
})

const currentRooms = computed(() => {
  if (!selectedFloor.value) return []
  return availableFloors.value.find(f => f.number === selectedFloor.value)?.rooms || []
})

// Методы
const openRoomEdit = (room) => {
  selectedRoom.value = room
  showRoomDialog.value = true
}

const addResident = () => {
  if (newResident.name && newResident.moveInDate) {
    selectedRoom.value.residents.push({ ...newResident })
    Object.assign(newResident, { name: '', moveInDate: null, contact: '' })
    showResidentDialog.value = false
  }
}

const addFurniture = () => {
  if (newFurniture.name) {
    selectedRoom.value.furniture.push({ ...newFurniture })
    Object.assign(newFurniture, { name: '', count: 1 })
  }
}

const deleteFurniture = (index) => {
  selectedRoom.value.furniture.splice(index, 1)
}
</script>

<template>
  <div class="p-4">
    <div class="flex gap-3 mb-4">
      <Dropdown 
        v-model="selectedBuilding" 
        :options="dormData.buildings" 
        optionLabel="name" 
        optionValue="id" 
        placeholder="Выберите здание" 
        class="w-15rem"
      />
      
      <Dropdown 
        v-model="selectedFloor" 
        :options="availableFloors" 
        optionLabel="number" 
        optionValue="number" 
        placeholder="Выберите этаж" 
        :disabled="!selectedBuilding"
        class="w-15rem"
      />
    </div>

    <div class="grid grid-nogutter gap-3">
      <Card v-for="room in currentRooms" :key="room.id" class="col-3">
        <template #title>Комната #{{ room.id }}</template>
        <template #subtitle>
          <Tag :value="room.status === 'free' ? 'Свободна' : 'Занята'" 
               :severity="room.status === 'free' ? 'success' : 'danger'" />
        </template>
        <template #content>
          <p>Вместимость: {{ room.capacity }}</p>
          
          <Divider />
          <div class="text-sm font-bold mb-2">Мебель:</div>
          <Chip v-for="(item, index) in room.furniture" :key="index" class="mr-2 mb-2">
            {{ item.name }} ({{ item.count }})
          </Chip>
          
          <Divider />
          <div class="text-sm font-bold mb-2">Жильцы:</div>
          <div v-for="(resident, index) in room.residents" :key="index" class="text-sm">
            {{ resident.name }} ({{ resident.moveInDate?.toLocaleDateString() }})
          </div>
        </template>
        <template #footer>
          <div class="flex gap-2">
            <Button label="Редактировать" icon="pi pi-pencil" @click="openRoomEdit(room)" />
            <Button label="Заселить" icon="pi pi-user-plus" severity="success" 
                    @click="showResidentDialog = true; selectedRoom = room" />
          </div>
        </template>
      </Card>
    </div>

    <!-- Диалог редактирования комнаты -->
    <Dialog v-model:visible="showRoomDialog" header="Редактирование комнаты" :style="{ width: '600px' }">
      <div class="p-fluid">
        <div class="field">
          <label>Статус</label>
          <SelectButton v-model="selectedRoom.status" :options="['free', 'occupied']">
            <template #option="slotProps">
              {{ slotProps.option === 'free' ? 'Свободна' : 'Занята' }}
            </template>
          </SelectButton>
        </div>

        <div class="field">
          <label>Добавить мебель</label>
          <div class="flex gap-2">
            <InputText v-model="newFurniture.name" placeholder="Название" />
            <InputNumber v-model="newFurniture.count" :min="1" />
            <Button label="Добавить" @click="addFurniture" />
          </div>
        </div>

        <DataTable :value="selectedRoom.furniture">
          <Column field="name" header="Мебель"></Column>
          <Column field="count" header="Количество"></Column>
          <Column header="Действия">
            <template #body="{ index }">
              <Button icon="pi pi-trash" severity="danger" @click="deleteFurniture(index)" />
            </template>
          </Column>
        </DataTable>
      </div>
    </Dialog>

    <!-- Диалог регистрации жильца -->
    <Dialog v-model:visible="showResidentDialog" header="Регистрация жильца" :style="{ width: '500px' }">
      <div class="p-fluid">
        <div class="field">
          <label>ФИО</label>
          <InputText v-model="newResident.name" required />
        </div>
        
        <div class="field">
          <label>Дата заселения</label>
          <Calendar v-model="newResident.moveInDate" dateFormat="dd.mm.yy" />
        </div>
        
        <div class="field">
          <label>Контактные данные</label>
          <InputText v-model="newResident.contact" />
        </div>
        
        <Button label="Зарегистрировать" icon="pi pi-check" @click="addResident" />
      </div>
    </Dialog>
  </div>
</template>

<style scoped>
.p-card {
  margin: 0.5rem;
  transition: transform 0.2s;
}

.p-card:hover {
  transform: translateY(-5px);
}
</style>
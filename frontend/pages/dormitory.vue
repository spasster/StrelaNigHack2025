<template>
  <div class="p-4 space-y-4">
    <h1 class="text-2xl font-bold">📐 Визуализация общежития</h1>

    <div class="flex items-center gap-4">
      <button @click="addRoom" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        ➕ Добавить комнату
      </button>
    </div>

    <v-stage :config="{ width: 1000, height: 600 }" class="border border-gray-300 rounded">
      <v-layer>
        <!-- Комнаты -->
        <v-rect
          v-for="room in rooms"
          :key="room.id"
          :config="{
            x: room.x,
            y: room.y,
            width: room.width,
            height: room.height,
            fill: room.occupied ? '#ef4444' : '#10b981',
            stroke: '#1f2937',
            strokeWidth: 1,
            cornerRadius: 6,
          }"
          @click="toggleOccupied(room)"
        />
        <!-- Текст -->
        <v-text
          v-for="room in rooms"
          :key="room.id + '_text'"
          :config="{
            x: room.x + 8,
            y: room.y + 8,
            text: room.number,
            fontSize: 14,
            fill: 'white',
            fontStyle: 'bold',
          }"
        />
      </v-layer>
    </v-stage>
  </div>
</template>

<script setup>
const rooms = ref([
  { id: 1, number: '101', x: 10, y: 10, width: 100, height: 60, occupied: false },
  { id: 2, number: '102', x: 120, y: 10, width: 100, height: 60, occupied: true },
])

// Добавление комнаты по сетке
const addRoom = () => {
  const newId = rooms.value.length + 1
  const columns = 8
  const col = (newId - 1) % columns
  const row = Math.floor((newId - 1) / columns)
  const spacingX = 110
  const spacingY = 70

  rooms.value.push({
    id: newId,
    number: `10${newId}`,
    x: 10 + col * spacingX,
    y: 100 + row * spacingY,
    width: 100,
    height: 60,
    occupied: false,
  })
}

// Переключение занятости
const toggleOccupied = (room) => {
  room.occupied = !room.occupied
}
</script>

<style scoped>
/* Можно добавить стили тут */
</style>

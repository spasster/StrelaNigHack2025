<!-- pages/dormitory.vue -->
<script setup>

const activeTab = ref('rooms')
</script>

<template>
  <div class="p-4">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Панель администратора</h1>
      <div class="flex gap-2">
        <Button label="Комнаты" icon="pi pi-home" @click="activeTab = 'rooms'" 
                :severity="activeTab === 'rooms' ? 'primary' : 'secondary'" />
        <Button label="Заселение" icon="pi pi-users" @click="activeTab = 'check-in'"
                :severity="activeTab === 'check-in' ? 'primary' : 'secondary'" />
      </div>
    </div>

    <div class="mt-4">
      <RoomsManager v-if="activeTab === 'rooms'" />
      <CheckInManager v-else-if="activeTab === 'check-in'" />
    </div>
  </div>
</template>

<style scoped>
.p-button {
  min-width: 120px;
}
</style>
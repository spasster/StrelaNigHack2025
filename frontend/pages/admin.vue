<!-- pages/admin.vue -->
<script setup>
const activeTab = ref('rooms')
const tabs = [
  { label: 'Комнаты', value: 'rooms', icon: 'pi pi-home' },
  { label: 'Заселение', value: 'check-in', icon: 'pi pi-users' },
  { label: 'Счета', value: 'bills', icon: 'pi pi-money-bill' },
  { label: 'Отчеты', value: 'reports', icon: 'pi pi-chart-bar' }
]
</script>

<template>
  <div class="p-4">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-white">Панель администратора</h1>
      <div class="flex gap-2">
        <Button 
          v-for="tab in tabs" 
          :key="tab.value"
          :label="tab.label" 
          :icon="tab.icon" 
          @click="activeTab = tab.value" 
          :severity="activeTab === tab.value ? 'primary' : 'secondary'"
          class="min-w-[120px]"
        />
      </div>
    </div>

    <div class="mt-4">
      <RoomsManager v-if="activeTab === 'rooms'" />
      <CheckInManager v-else-if="activeTab === 'check-in'" />
      <BillsManager v-else-if="activeTab === 'bills'" />
      <ReportsManager v-else-if="activeTab === 'reports'" />
    </div>
  </div>
</template>

<style scoped>
.p-button {
  @apply transition-colors duration-200;
}
</style>
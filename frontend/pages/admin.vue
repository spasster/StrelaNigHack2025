<!-- pages/admin.vue -->
<script setup>
const activeTab = ref('checkins')

const tabs = [
  { id: 'checkins', label: 'Заселения', icon: 'pi pi-home' },
  { id: 'rooms', label: 'Комнаты', icon: 'pi pi-building' },
  { id: 'reports', label: 'Отчеты', icon: 'pi pi-chart-bar' }
]

const activeTabLabel = computed(() => {
  return tabs.find(tab => tab.id === activeTab.value)?.label || ''
})

const activeTabIcon = computed(() => {
  return tabs.find(tab => tab.id === activeTab.value)?.icon || ''
})
</script>

<template>
  <div class="min-h-screen text-white">
    <div class="container mx-auto px-4 py-8">
      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Левая панель -->
        <div class="w-full lg:w-1/4">
          <Card class="bg-custom-card border-none">
            <template #title>
              <div class="flex items-center gap-2">
                <i class="pi pi-user text-primary"></i>
                <span>Администратор</span>
              </div>
            </template>
            <template #content>
              <div class="flex flex-col gap-4">
                <Button 
                  v-for="tab in tabs" 
                  :key="tab.id"
                  :label="tab.label"
                  :icon="tab.icon"
                  :severity="activeTab === tab.id ? 'primary' : 'secondary'"
                  class="w-full justify-start"
                  @click="activeTab = tab.id"
                />
              </div>
            </template>
          </Card>
        </div>

        <!-- Правая панель -->
        <div class="w-full lg:w-3/4">
          <Card class="bg-custom-card border-none">
            <template #title>
              <div class="flex items-center gap-2">
                <i :class="activeTabIcon" class="text-primary"></i>
                <span>{{ activeTabLabel }}</span>
              </div>
            </template>
            <template #content>
              <div class="space-y-6">
                <!-- Компоненты -->
                <CheckInManager v-if="activeTab === 'checkins'" />
                <RoomsManager v-if="activeTab === 'rooms'" />
                <ReportsManager v-if="activeTab === 'reports'" />
              </div>
            </template>
          </Card>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1400px;
}

@media (max-width: 1024px) {
  .container {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}

@media (max-width: 768px) {
  .container {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }
}
</style>
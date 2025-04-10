<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-xl font-semibold text-white">Управление обращениями</h2>
      <Select
        v-model="selectedStatus"
        :options="statusOptions"
        optionLabel="label"
        optionValue="value"
        placeholder="Фильтр по статусу"
        class="w-48"
      />
    </div>

    <div v-if="loading" class="flex justify-center items-center h-64">
      <ProgressSpinner />
    </div>

    <div v-else-if="!appeals.length" class="flex flex-col items-center justify-center h-64 text-white/60">
      <i class="pi pi-inbox text-4xl mb-2"></i>
      <p class="text-lg">Обращений пока нет</p>
    </div>

    <DataTable
      v-else
      :value="filteredAppeals"
      :paginator="true"
      :rows="10"
      :rowsPerPageOptions="[5, 10, 20, 50]"
      :loading="loading"
      stripedRows
      class="p-datatable-sm"
    >
      <Column field="id" header="ID" sortable></Column>
      <Column field="user" header="Пользователь" sortable>
        <template #body="{ data }">
          {{ data.user?.name || 'Не указано' }}
        </template>
      </Column>
      <Column field="category" header="Категория" sortable>
        <template #body="{ data }">
          {{ getCategoryLabel(data.category) }}
        </template>
      </Column>
      <Column field="description" header="Описание">
        <template #body="{ data }">
          <div class="max-w-xs truncate">{{ data.description }}</div>
        </template>
      </Column>
      <Column field="status" header="Статус" sortable>
        <template #body="{ data }">
          <Tag
            :severity="getStatusSeverity(data.status)"
            :value="getStatusLabel(data.status)"
          />
        </template>
      </Column>
      <Column field="created_at" header="Дата создания" sortable>
        <template #body="{ data }">
          {{ formatDate(data.created_at) }}
        </template>
      </Column>
      <Column header="Действия">
        <template #body="{ data }">
          <div class="flex gap-2">
            <Button
              icon="pi pi-eye"
              severity="info"
              text
              @click="openDetails(data)"
            />
            <Button
              icon="pi pi-check"
              severity="success"
              text
              @click="updateStatus(data, 'completed')"
              v-if="data.status !== 'completed'"
            />
            <Button
              icon="pi pi-times"
              severity="danger"
              text
              @click="deleteAppeal(data)"
            />
          </div>
        </template>
      </Column>
    </DataTable>

    <!-- Диалог просмотра обращения -->
    <Dialog
      v-model:visible="showDetails"
      modal
      :style="{ width: '600px' }"
      class="bg-custom-card border-none font-paratype m-2"
    >
      <template #header>
        <h2 class="text-xl text-white font-semibold">Детали обращения</h2>
      </template>

      <div v-if="selectedAppeal" class="space-y-4">
        <div>
          <label class="block text-white/80 mb-1">Пользователь</label>
          <div class="bg-gray-700 text-white p-2 rounded">
            {{ selectedAppeal.user?.name || 'Не указано' }}
          </div>
        </div>

        <div>
          <label class="block text-white/80 mb-1">Категория</label>
          <div class="bg-gray-700 text-white p-2 rounded">
            {{ getCategoryLabel(selectedAppeal.category) }}
          </div>
        </div>

        <div>
          <label class="block text-white/80 mb-1">Описание</label>
          <div class="bg-gray-700 text-white p-2 rounded">
            {{ selectedAppeal.description }}
          </div>
        </div>

        <div v-if="selectedAppeal.image_base64">
          <label class="block text-white/80 mb-1">Фотографии</label>
          <div class="grid grid-cols-2 gap-2">
            <div 
              class="relative group cursor-pointer"
              @click="showImageModal = true"
            >
              <img
                :src="selectedAppeal.image_base64"
                class="w-full h-32 object-cover rounded"
              />
              <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                <i class="pi pi-search-plus text-white text-2xl"></i>
              </div>
            </div>
          </div>
        </div>

        <div>
          <label class="block text-white/80 mb-1">Статус</label>
          <Select
            v-model="selectedAppeal.status"
            :options="statusOptions"
            optionLabel="label"
            optionValue="value"
            class="w-full"
          />
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-2">
          <Button
            label="Отмена"
            severity="secondary"
            @click="showDetails = false"
          />
          <Button
            label="Сохранить"
            @click="saveAppeal"
          />
        </div>
      </template>
    </Dialog>

    <!-- Модальное окно для просмотра изображения -->
    <Dialog
      v-model:visible="showImageModal"
      modal
      :style="{ width: '90vw', maxWidth: '1200px' }"
      class="bg-custom-card border-none m-2"
    >
 

      <div class="flex justify-center items-center h-[80vh]">
        <img
          :src="selectedAppeal?.image_base64"
          class="max-h-full max-w-full object-contain"
        />
      </div>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useToast } from 'primevue/usetoast';
import { useFetch } from '~/composables/useFetch';
import type { Appeal } from '~/types/appeals';

const toast = useToast();
const { fetchWithAuth } = useFetch();

const loading = ref(false);
const appeals = ref<Appeal[]>([]);
const selectedStatus = ref<string | null>(null);
const showDetails = ref(false);
const selectedAppeal = ref<Appeal | null>(null);
const showImageModal = ref(false);

const statusOptions = [
  { label: 'Все', value: null },
  { label: 'В ожидании', value: 'pending' },
  { label: 'В работе', value: 'in_progress' },
  { label: 'Выполнено', value: 'completed' }
];

const categories = [
  { label: 'Электрика', value: 'electricity' },
  { label: 'Сантехника', value: 'plumbing' },
  { label: 'Мебель', value: 'furniture' },
  { label: 'Другое', value: 'other' }
];

const filteredAppeals = computed(() => {
  if (!selectedStatus.value) return appeals.value;
  return appeals.value.filter(appeal => appeal.status === selectedStatus.value);
});

const loadAppeals = async () => {
  loading.value = true;
  try {
    const response = await fetchWithAuth('/api/appeals/');
    appeals.value = await response.json();
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось загрузить обращения',
      life: 3000
    });
    appeals.value = [];
  } finally {
    loading.value = false;
  }
};

const getCategoryLabel = (value: Appeal['category']) => {
  return categories.find(c => c.value === value)?.label || value;
};

const getStatusLabel = (status: Appeal['status']) => {
  switch (status) {
    case 'pending': return 'В ожидании';
    case 'in_progress': return 'В работе';
    case 'completed': return 'Выполнено';
    default: return status;
  }
};

const getStatusSeverity = (status: Appeal['status']) => {
  switch (status) {
    case 'pending': return 'warning';
    case 'in_progress': return 'info';
    case 'completed': return 'success';
    default: return 'info';
  }
};

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('ru-RU');
};

const openDetails = (appeal: Appeal) => {
  selectedAppeal.value = { ...appeal };
  showDetails.value = true;
};

const updateStatus = async (appeal: Appeal, status: Appeal['status']) => {
  try {
    await fetchWithAuth(`/api/appeals/${appeal.id}/update_status/`, {
      method: 'PATCH',
      body: JSON.stringify({ status })
    });
    
    toast.add({
      severity: 'success',
      summary: 'Успех',
      detail: 'Статус обновлен',
      life: 3000
    });
    
    await loadAppeals();
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось обновить статус',
      life: 3000
    });
  }
};

const deleteAppeal = async (appeal: Appeal) => {
  try {
    await fetchWithAuth(`/api/appeals/${appeal.id}/`, {
      method: 'DELETE'
    });
    
    toast.add({
      severity: 'success',
      summary: 'Успех',
      detail: 'Обращение удалено',
      life: 3000
    });
    
    await loadAppeals();
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось удалить обращение',
      life: 3000
    });
  }
};

const saveAppeal = async () => {
  if (!selectedAppeal.value) return;

  try {
    await fetchWithAuth(`/api/appeals/${selectedAppeal.value.id}/update_status/`, {
      method: 'PATCH',
      body: JSON.stringify({
        status: selectedAppeal.value.status
      })
    });
    
    toast.add({
      severity: 'success',
      summary: 'Успех',
      detail: 'Обращение обновлено',
      life: 3000
    });
    
    showDetails.value = false;
    await loadAppeals();
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось обновить обращение',
      life: 3000
    });
  }
};

onMounted(() => {
  loadAppeals();
});
</script>

<style scoped>
:deep(.p-datatable) {
  @apply bg-custom-card text-white;
}

:deep(.p-datatable-header) {
  @apply bg-custom-card text-white;
}

:deep(.p-datatable-thead > tr > th) {
  @apply bg-gray-700 text-white;
}

:deep(.p-datatable-tbody > tr) {
  @apply bg-custom-card text-white;
}

:deep(.p-datatable-tbody > tr:hover) {
  @apply bg-gray-700;
}

:deep(.p-paginator) {
  @apply bg-custom-card text-white;
}

:deep(.p-dropdown) {
  @apply w-full;
}

:deep(.p-dialog-content) {
  @apply bg-custom-card;
  padding: 0 !important;
}

:deep(.p-progress-spinner) {
  @apply w-12 h-12;
}
</style> 
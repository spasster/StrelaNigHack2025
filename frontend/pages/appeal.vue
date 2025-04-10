<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold mb-6 text-custom-text">Обращения</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Форма создания обращения -->
      <Card class="bg-custom-card border-none">
        <template #title>
          <div class="text-xl font-bold text-custom-text">Создать обращение</div>
        </template>
        <template #content>
          <form @submit.prevent="submitAppeal" class="space-y-4">
            <div class="field">
              <label class="block text-custom-text mb-2">Категория</label>
              <Dropdown
                v-model="form.category"
                :options="categories"
                optionLabel="label"
                optionValue="value"
                placeholder="Выберите категорию"
                class="w-full"
              />
            </div>

            <div class="field">
              <label class="block text-custom-text mb-2">Описание</label>
              <Textarea
                v-model="form.description"
                rows="5"
                placeholder="Опишите проблему"
                class="w-full"
              />
            </div>

            <div class="field">
              <label class="block text-custom-text mb-2">Фотография (опционально)</label>
              <FileUpload
                mode="basic"
                accept="image/*"
                :maxFileSize="1000000"
                chooseLabel="Выбрать фото"
                @select="onFileSelect"
              />
            </div>

            <Button
              type="submit"
              label="Отправить"
              class="w-full"
              :loading="loading"
            />
          </form>
        </template>
      </Card>

      <!-- Список обращений -->
      <Card class="bg-custom-card border-none">
        <template #title>
          <div class="text-xl font-bold text-custom-text">Мои обращения</div>
        </template>
        <template #content>
          <div v-if="loading" class="flex justify-center">
            <ProgressSpinner />
          </div>
          <div v-else-if="appeals.length === 0" class="text-center text-custom-text">
            У вас пока нет обращений
          </div>
          <div v-else class="space-y-4">
            <div
              v-for="appeal in appeals"
              :key="appeal.id"
              class="p-4 rounded-lg border border-custom-border"
            >
              <div class="flex justify-between items-start mb-2">
                <div>
                  <span class="font-bold text-custom-text">{{ getCategoryLabel(appeal.category) }}</span>
                  <span class="ml-2 text-sm" :class="getStatusClass(appeal.status)">
                    {{ getStatusLabel(appeal.status) }}
                  </span>
                </div>
                <span class="text-sm text-custom-text">
                  {{ formatDate(appeal.created_at) }}
                </span>
              </div>
              <p class="text-custom-text mb-2">{{ appeal.description }}</p>
              <div v-if="appeal.images?.length" class="flex gap-2">
                <img
                  v-for="image in appeal.images"
                  :key="image.id"
                  :src="image.image"
                  class="w-20 h-20 object-cover rounded"
                  @click="openImage(image.image)"
                />
              </div>
            </div>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useToast } from 'primevue/usetoast';
import { useFetch } from '~/composables/useFetch';
import type { Appeal, AppealForm } from '~/types/appeals';

const toast = useToast();
const { fetchWithAuth } = useFetch();

const loading = ref(false);
const appeals = ref<Appeal[]>([]);
const form = ref<AppealForm>({
  category: 'electricity',
  description: '',
  image_base64: undefined
});

const categories = [
  { label: 'Электрика', value: 'electricity' as const },
  { label: 'Сантехника', value: 'plumbing' as const },
  { label: 'Мебель', value: 'furniture' as const },
  { label: 'Другое', value: 'other' as const }
];

const statuses = {
  pending: { label: 'В ожидании', class: 'text-yellow-500' },
  in_progress: { label: 'В процессе', class: 'text-blue-500' },
  completed: { label: 'Завершено', class: 'text-green-500' }
} as const;

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
  } finally {
    loading.value = false;
  }
};

const submitAppeal = async () => {
  if (!form.value.category || !form.value.description) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Заполните все обязательные поля',
      life: 3000
    });
    return;
  }

  loading.value = true;
  try {
    await fetchWithAuth('/api/appeals/', {
      method: 'POST',
      body: JSON.stringify(form.value)
    });
    
    toast.add({
      severity: 'success',
      summary: 'Успех',
      detail: 'Обращение успешно создано',
      life: 3000
    });
    
    form.value = {
      category: 'electricity',
      description: '',
      image_base64: undefined
    };
    
    await loadAppeals();
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось создать обращение',
      life: 3000
    });
  } finally {
    loading.value = false;
  }
};

const onFileSelect = (event: any) => {
  const file = event.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      if (e.target?.result) {
        form.value.image_base64 = e.target.result as string;
      }
    };
    reader.readAsDataURL(file);
  }
};

const getCategoryLabel = (value: Appeal['category']) => {
  return categories.find(c => c.value === value)?.label || value;
};

const getStatusLabel = (status: Appeal['status']) => {
  return statuses[status]?.label || status;
};

const getStatusClass = (status: Appeal['status']) => {
  return statuses[status]?.class || '';
};

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('ru-RU');
};

const openImage = (url: string) => {
  window.open(url, '_blank');
};

onMounted(() => {
  loadAppeals();
});
</script>

<style scoped>
.field {
  @apply mb-4;
}

:deep(.p-card) {
  @apply shadow-lg;
}

:deep(.p-dropdown) {
  @apply w-full;
}

:deep(.p-textarea) {
  @apply w-full;
}

:deep(.p-fileupload) {
  @apply w-full;
}
</style>
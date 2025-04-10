<!-- components/ReportsManager.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useFetch } from '~/composables/useFetch'
import { useToast } from 'primevue/usetoast'

const toast = useToast()
const { fetchWithAuth } = useFetch()
const loading = ref(false)
const reports = ref({
  occupancy: null,
  checkin: null,
  university: null
})

const loadReports = async () => {
  loading.value = true
  try {
    const [occupancyResponse, checkinResponse, universityResponse] = await Promise.all([
      fetchWithAuth('/api/rooms/reports/occupancy/'),
      fetchWithAuth('/api/rooms/reports/checkin/'),
      fetchWithAuth('/api/rooms/reports/university/')
    ])

    const occupancyData = await occupancyResponse.json()
    const checkinData = await checkinResponse.json()
    const universityData = await universityResponse.json()

    reports.value = {
      occupancy: occupancyData,
      checkin: checkinData,
      university: universityData
    }
  } catch (error) {
    console.error('Ошибка при загрузке отчетов:', error)
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось загрузить отчеты',
      life: 3000
    })
  } finally {
    loading.value = false
  }
}

const exportReport = async (type) => {
  try {
    const response = await fetchWithAuth(`/api/rooms/reports/export/?report_type=${type}`)
    if (response.ok) {
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `report_${type}.xlsx`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      
      toast.add({
        severity: 'success',
        summary: 'Успех',
        detail: 'Отчет успешно экспортирован',
        life: 3000
      })
    } else {
      throw new Error('Ошибка при экспорте отчета')
    }
  } catch (error) {
    console.error('Ошибка при экспорте отчета:', error)
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось экспортировать отчет',
      life: 3000
    })
  }
}

onMounted(() => {
  loadReports()
})
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-2xl font-semibold text-white">Отчеты</h2>
      <div class="flex gap-2">
        <Button 
          label="Экспорт всех отчетов" 
          icon="pi pi-download" 
          @click="exportReport('all')" 
          severity="info"
        />
      </div>
    </div>

    <div v-if="loading" class="flex items-center justify-center p-8">
      <i class="pi pi-spinner pi-spin mr-2"></i>
      <span>Загрузка отчетов...</span>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Отчет по заполняемости -->
      <Card class="bg-black/75 border-none">
        <template #title>
          <div class="flex justify-between items-center">
            <span>Заполняемость комнат</span>
            <Button 
              icon="pi pi-download" 
              @click="exportReport('occupancy')" 
              text
            />
          </div>
        </template>
        <template #content>
          <div v-if="reports.occupancy" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div class="p-4 bg-black/50 rounded-lg">
                <div class="text-sm text-gray-400">Всего комнат</div>
                <div class="text-2xl font-bold">{{ reports.occupancy.total_rooms }}</div>
              </div>
              <div class="p-4 bg-black/50 rounded-lg">
                <div class="text-sm text-gray-400">Занято</div>
                <div class="text-2xl font-bold">{{ reports.occupancy.occupied_rooms }}</div>
              </div>
              <div class="p-4 bg-black/50 rounded-lg">
                <div class="text-sm text-gray-400">Свободно</div>
                <div class="text-2xl font-bold">{{ reports.occupancy.free_rooms }}</div>
              </div>
              <div class="p-4 bg-black/50 rounded-lg">
                <div class="text-sm text-gray-400">Заполняемость</div>
                <div class="text-2xl font-bold">{{ (reports.occupancy.occupancy_rate * 100).toFixed(1) }}%</div>
              </div>
            </div>
            <div v-if="reports.occupancy.rooms_by_gender" class="mt-4">
              <h3 class="text-lg font-semibold mb-2">Распределение по полу</h3>
              <div class="grid grid-cols-2 gap-4">
                <div class="p-4 bg-black/50 rounded-lg">
                  <div class="text-sm text-gray-400">Мужские комнаты</div>
                  <div class="text-2xl font-bold">{{ reports.occupancy.rooms_by_gender.M || 0 }}</div>
                </div>
                <div class="p-4 bg-black/50 rounded-lg">
                  <div class="text-sm text-gray-400">Женские комнаты</div>
                  <div class="text-2xl font-bold">{{ reports.occupancy.rooms_by_gender.F || 0 }}</div>
                </div>
              </div>
            </div>
          </div>
        </template>
      </Card>

      <!-- Отчет по срокам проживания -->
      <Card class="bg-black/75 border-none">
        <template #title>
          <div class="flex justify-between items-center">
            <span>Сроки проживания</span>
            <Button 
              icon="pi pi-download" 
              @click="exportReport('checkin')" 
              text
            />
          </div>
        </template>
        <template #content>
          <div v-if="reports.checkin" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div class="p-4 bg-black/50 rounded-lg">
                <div class="text-sm text-gray-400">Всего студентов</div>
                <div class="text-2xl font-bold">{{ reports.checkin.total_students }}</div>
              </div>
              <div class="p-4 bg-black/50 rounded-lg">
                <div class="text-sm text-gray-400">Средний срок</div>
                <div class="text-2xl font-bold">{{ reports.checkin.average_stay_duration.toFixed(1) }} дн.</div>
              </div>
            </div>
            <div v-if="reports.checkin.students_by_duration" class="mt-4">
              <h3 class="text-lg font-semibold mb-2">Распределение по срокам</h3>
              <div class="space-y-2">
                <div v-for="(count, duration) in reports.checkin.students_by_duration" 
                     :key="duration"
                     class="p-4 bg-black/50 rounded-lg">
                  <div class="text-sm text-gray-400">{{ duration }} дней</div>
                  <div class="text-xl font-bold">{{ count }} студентов</div>
                </div>
              </div>
            </div>
          </div>
        </template>
      </Card>

      <!-- Отчет по университетам -->
      <Card class="bg-black/75 border-none md:col-span-2">
        <template #title>
          <div class="flex justify-between items-center">
            <span>Распределение по университетам</span>
            <Button 
              icon="pi pi-download" 
              @click="exportReport('university')" 
              text
            />
          </div>
        </template>
        <template #content>
          <div v-if="reports.university" class="space-y-4">
            <div v-for="univ in reports.university" :key="univ.university" class="p-4 bg-black/50 rounded-lg">
              <div class="text-lg font-bold mb-2">{{ univ.university }}</div>
              <div class="text-sm text-gray-400 mb-2">Всего студентов: {{ univ.total_students }}</div>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <div class="text-sm font-bold mb-1">Факультеты</div>
                  <div v-for="(count, faculty) in univ.faculties" :key="faculty" class="text-sm">
                    {{ faculty }}: {{ count }}
                  </div>
                </div>
                <div>
                  <div class="text-sm font-bold mb-1">Курсы</div>
                  <div v-for="(count, course) in univ.courses" :key="course" class="text-sm">
                    {{ course }} курс: {{ count }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template> 
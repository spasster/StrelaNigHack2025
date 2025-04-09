<!-- components/BillsManager.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useFetch } from '~/composables/useFetch'
import { useToast } from 'primevue/usetoast'

const toast = useToast()
const { fetchWithAuth } = useFetch()
const filters = ref({
  global: { value: null, matchMode: 'contains' }
})

const bills = ref([])
const loading = ref(false)
const selectedBill = ref(null)
const showBillDialog = ref(false)
const showPaymentDialog = ref(false)

const billForm = ref({
  resident: null,
  amount: null,
  bill_type: 'RENT',
  due_date: null
})

const editingBill = ref(null)

const paymentForm = ref({
  bill: null,
  amount: null,
  payment_method: 'CARD',
  transaction_id: '',
  status: 'SUCCESS'
})

const loadBills = async () => {
  loading.value = true
  try {
    const response = await fetchWithAuth('/api/bills/bills/')
    const data = await response.json()
    bills.value = data
  } catch (error) {
    console.error('Ошибка при загрузке счетов:', error)
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось загрузить список счетов',
      life: 3000
    })
  } finally {
    loading.value = false
  }
}

const openBillDialog = (bill = null) => {
  editingBill.value = bill
  if (bill) {
    billForm.value = { ...bill }
  } else {
    billForm.value = {
      resident: null,
      amount: null,
      bill_type: 'RENT',
      due_date: null
    }
  }
  showBillDialog.value = true
}

const saveBill = async () => {
  // Проверяем заполнение обязательных полей
  if (!billForm.value.resident) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Укажите жильца',
      life: 3000
    })
    return
  }

  if (!billForm.value.amount || billForm.value.amount <= 0) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Укажите корректную сумму',
      life: 3000
    })
    return
  }

  if (!billForm.value.due_date) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Укажите срок оплаты',
      life: 3000
    })
    return
  }

  try {
    const url = editingBill.value 
      ? `/api/bills/bills/${editingBill.value}/` 
      : '/api/bills/bills/'
    const method = editingBill.value ? 'PUT' : 'POST'
    
    const response = await fetchWithAuth(url, {
      method,
      body: JSON.stringify({
        resident: billForm.value.resident,
        amount: billForm.value.amount,
        bill_type: billForm.value.bill_type,
        due_date: formatDate(billForm.value.due_date)
      })
    })
    
    if (response.ok) {
      toast.add({ 
        severity: 'success', 
        summary: 'Успех', 
        detail: 'Счет сохранен', 
        life: 3000 
      })
      closeBillDialog()
      loadBills()
    } else {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Ошибка при сохранении счета')
    }
  } catch (error) {
    console.error('Ошибка при сохранении счета:', error)
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: error.message || 'Не удалось сохранить счет',
      life: 3000
    })
  }
}

// Добавляем функцию форматирования даты
const formatDate = (date) => {
  if (!date) return null
  const d = new Date(date)
  return d.toISOString().split('T')[0]
}

const closeBillDialog = () => {
  showBillDialog.value = false
  editingBill.value = null
  billForm.value = {
    resident: null,
    amount: null,
    bill_type: 'RENT',
    due_date: null
  }
}

const openPaymentDialog = (bill) => {
  if (!bill || !bill.id) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Неверные данные счета',
      life: 3000
    })
    return
  }

  selectedBill.value = bill
  paymentForm.value = {
    bill: bill.id,
    amount: bill.amount,
    payment_method: 'CARD',
    transaction_id: '',
    status: 'SUCCESS'
  }
  showPaymentDialog.value = true
}

const createPayment = async () => {
  if (!paymentForm.value.bill) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'ID счета не указан',
      life: 3000
    })
    return
  }

  try {
    const response = await fetchWithAuth('/api/bills/payments/', {
      method: 'POST',
      body: JSON.stringify({
        bill: paymentForm.value.bill,
        amount: paymentForm.value.amount,
        payment_method: paymentForm.value.payment_method,
        transaction_id: paymentForm.value.transaction_id,
        status: paymentForm.value.status
      })
    })
    
    if (response.ok) {
      toast.add({ 
        severity: 'success', 
        summary: 'Успех', 
        detail: 'Платеж создан', 
        life: 3000 
      })
      closePaymentDialog()
      loadBills()
    } else {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Ошибка при создании платежа')
    }
  } catch (error) {
    console.error('Ошибка при создании платежа:', error)
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: error.message || 'Не удалось создать платеж',
      life: 3000
    })
  }
}

const closePaymentDialog = () => {
  showPaymentDialog.value = false
  selectedBill.value = null
  paymentForm.value = {
    bill: null,
    amount: null,
    payment_method: 'CARD',
    transaction_id: '',
    status: 'SUCCESS'
  }
}

const deleteBill = async (id) => {
  if (!id) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'ID счета не указан',
      life: 3000
    })
    return
  }

  try {
    const response = await fetchWithAuth(`/api/bills/bills/${id}/`, {
      method: 'DELETE'
    })
    
    if (response.ok) {
      toast.add({ 
        severity: 'success', 
        summary: 'Успех', 
        detail: 'Счет удален', 
        life: 3000 
      })
      loadBills()
    } else {
      throw new Error('Ошибка при удалении счета')
    }
  } catch (error) {
    console.error('Ошибка при удалении счета:', error)
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось удалить счет',
      life: 3000
    })
  }
}

onMounted(() => {
  loadBills()
})
</script>

<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center">
      <h2 class="text-2xl font-semibold text-white">Управление счетами</h2>
      <Button 
        label="Создать счет" 
        icon="pi pi-plus" 
        @click="openBillDialog" 
        severity="success"
      />
    </div>

    <DataTable 
      :value="bills" 
      :loading="loading"
      class="p-datatable-sm"
      :pt="{
        root: { class: 'bg-black/75 border-none rounded-lg' },
        header: { class: 'bg-black/75 border-none' },
        thead: { class: 'bg-black/75' },
        tbody: { class: 'bg-black/75' },
        tfoot: { class: 'bg-black/75 border-none' }
      }"
    >
      <template #header>
        <div class="flex justify-between items-center">
          <span class="p-input-icon-left">
            <i class="pi pi-search" />
            <InputText 
              v-model="filters['global'].value" 
              placeholder="Поиск..." 
              class="w-full"
            />
          </span>
        </div>
      </template>

      <template #loading>
        <div class="flex items-center justify-center p-4">
          <i class="pi pi-spinner pi-spin mr-2"></i>
          <span>Загрузка...</span>
        </div>
      </template>

      <template #empty>
        <div class="flex items-center justify-center p-4">
          <i class="pi pi-info-circle mr-2"></i>
          <span>Нет данных для отображения</span>
        </div>
      </template>

      <Column field="id" header="ID" sortable />
      <Column field="resident" header="Жилец" sortable />
      <Column field="amount" header="Сумма" sortable>
        <template #body="{ data }">
          {{ data.amount }} ₽
        </template>
      </Column>
      <Column field="bill_type" header="Тип" sortable>
        <template #body="{ data }">
          <Tag 
            :value="data.bill_type" 
            :severity="data.bill_type === 'RENT' ? 'success' : data.bill_type === 'UTILITIES' ? 'info' : 'warning'"
          />
        </template>
      </Column>
      <Column field="status" header="Статус" sortable>
        <template #body="{ data }">
          <Tag 
            :value="data.status" 
            :severity="data.status === 'PAID' ? 'success' : data.status === 'PENDING' ? 'warning' : 'danger'"
          />
        </template>
      </Column>
      <Column field="due_date" header="Срок оплаты" sortable>
        <template #body="{ data }">
          {{ new Date(data.due_date).toLocaleDateString() }}
        </template>
      </Column>
      <Column header="Действия">
        <template #body="{ data }">
          <div class="flex gap-2">
            <Button 
              icon="pi pi-pencil" 
              @click="openBillDialog(data)" 
              severity="info"
              text
            />
            <Button 
              icon="pi pi-trash" 
              @click="() => deleteBill(data.id)" 
              severity="danger"
              text
            />
            <Button 
              icon="pi pi-money-bill" 
              @click="openPaymentDialog(data)" 
              severity="success"
              text
            />
          </div>
        </template>
      </Column>
    </DataTable>

    <Dialog 
      v-model:visible="showBillDialog" 
      :modal="true"
      :style="{ width: '450px' }"
      :header="editingBill ? 'Редактирование счета' : 'Новый счет'"
      class="p-fluid"
    >
      <div class="field">
        <label for="resident" class="font-bold">Жилец</label>
        <InputNumber id="resident" v-model="billForm.resident" class="w-full" />
      </div>
      <div class="field">
        <label for="amount" class="font-bold">Сумма</label>
        <InputNumber id="amount" v-model="billForm.amount" class="w-full" />
      </div>
      <div class="field">
        <label for="bill_type" class="font-bold">Тип счета</label>
        <Dropdown 
          id="bill_type" 
          v-model="billForm.bill_type" 
          :options="['RENT', 'UTILITIES', 'OTHER']" 
          class="w-full"
        />
      </div>
      <div class="field">
        <label for="due_date" class="font-bold">Срок оплаты</label>
        <Calendar id="due_date" v-model="billForm.due_date" class="w-full" />
      </div>

      <template #footer>
        <Button label="Отмена" icon="pi pi-times" @click="closeBillDialog" text />
        <Button 
          label="Сохранить" 
          icon="pi pi-check" 
          @click="saveBill" 
          severity="success"
        />
      </template>
    </Dialog>

    <Dialog 
      v-model:visible="showPaymentDialog" 
      :modal="true"
      :style="{ width: '450px' }"
      header="Оплата"
      class="p-fluid"
    >
      <div class="field">
        <label for="amount" class="font-bold">Сумма</label>
        <InputNumber id="amount" v-model="paymentForm.amount" class="w-full" />
      </div>
      <div class="field">
        <label for="payment_method" class="font-bold">Способ оплаты</label>
        <Dropdown 
          id="payment_method" 
          v-model="paymentForm.payment_method" 
          :options="['CARD', 'CASH', 'TRANSFER']" 
          class="w-full"
        />
      </div>
      <div class="field">
        <label for="transaction_id" class="font-bold">ID транзакции</label>
        <InputText id="transaction_id" v-model="paymentForm.transaction_id" class="w-full" />
      </div>

      <template #footer>
        <Button label="Отмена" icon="pi pi-times" @click="closePaymentDialog" text />
        <Button 
          label="Оплатить" 
          icon="pi pi-check" 
          @click="createPayment" 
          severity="success"
        />
      </template>
    </Dialog>
  </div>
</template> 
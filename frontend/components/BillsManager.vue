<!-- components/BillsManager.vue -->
<script setup>
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
    const response = await fetch('/api/bills/', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    bills.value = await response.json()
  } catch (error) {
    console.error('Ошибка при загрузке счетов:', error)
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
  try {
    const url = editingBill.value 
      ? `/api/bills/${editingBill.value.id}/` 
      : '/api/bills/'
    const method = editingBill.value ? 'PUT' : 'POST'
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify(billForm.value)
    })
    
    if (response.ok) {
      toast.add({ severity: 'success', summary: 'Успех', detail: 'Счет сохранен', life: 3000 })
      closeBillDialog()
      loadBills()
    }
  } catch (error) {
    console.error('Ошибка при сохранении счета:', error)
  }
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
  try {
    const response = await fetch('/api/bills/payments/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(paymentForm.value)
    })
    if (response.ok) {
      toast.add({ severity: 'success', summary: 'Успех', detail: 'Платеж создан', life: 3000 })
      closePaymentDialog()
      loadBills()
    }
  } catch (error) {
    console.error('Ошибка при создании платежа:', error)
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
              @click="deleteBill(data.id)" 
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
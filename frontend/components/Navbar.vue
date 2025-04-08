<template>
  <nav class="w-full py-4 z-0">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <!-- Бургер меню -->
      <div class="flex items-center gap-1">
        <button 
          @click="visible = true"
          class="p-2 text-custom-yellow rounded-lg hover:bg-white transition-colors"
          aria-label="Открыть меню"
        >
          <svg 
            class="w-6 h-6" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              stroke-linecap="round" 
              stroke-linejoin="round" 
              stroke-width="2" 
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
        </button>
        <NuxtLink to="/" class="text-white text-lg hover:text-custom-yellow transition-colors">
          Главная
        </NuxtLink>
      </div>

      <!-- Drawer меню -->
      <Drawer v-model:visible="visible" position="left" :modal="true" class="bg-black/75 border-black">
        <template #container="{ closeCallback }">
          <div class="flex flex-col h-full bg-black/75">
            <div class="flex items-center justify-between px-6 pt-4 shrink-0">
              <span class="inline-flex items-center gap-2">
                <img src="/logo.png" alt="Logo" class="h-5 w-auto" />
              </span>
              <Button 
                type="button" 
                @click="closeCallback" 
                icon="pi pi-times" 
                rounded 
                outlined 
                class="text-custom-yellow hover:bg-custom-yellow hover:text-black transition-colors"
              />
            </div>
            <div class="overflow-y-auto">
              <ul class="list-none p-4 m-0">
                <li>
                  <NuxtLink 
                    to="/" 
                    class="flex items-center cursor-pointer p-4 rounded text-white hover:bg-custom-yellow hover:text-black duration-150 transition-colors"
                  >
                    <i class="pi pi-home mr-2"></i>
                    <span class="font-medium">Главная</span>
                  </NuxtLink>
                </li>
                <li>
                  <NuxtLink 
                    to="/catalog" 
                    class="flex items-center cursor-pointer p-4 rounded text-white hover:bg-custom-yellow hover:text-black duration-150 transition-colors"
                  >
                    <i class="pi pi-th-large mr-2"></i>
                    <span class="font-medium">Каталог</span>
                  </NuxtLink>
                </li>
                <li>
                  <NuxtLink 
                    to="/about" 
                    class="flex items-center cursor-pointer p-4 rounded text-white hover:bg-custom-yellow hover:text-black duration-150 transition-colors"
                  >
                    <i class="pi pi-info-circle mr-2"></i>
                    <span class="font-medium">О нас</span>
                  </NuxtLink>
                </li>
                <li>
                  <NuxtLink 
                    to="/contacts" 
                    class="flex items-center cursor-pointer p-4 rounded text-white hover:bg-custom-yellow hover:text-black duration-150 transition-colors"
                  >
                    <i class="pi pi-envelope mr-2"></i>
                    <span class="font-medium">Контакты</span>
                  </NuxtLink>
                </li>
              </ul>
            </div>
          </div>
        </template>
      </Drawer>

      <!-- Логотип -->
      <div class="absolute left-1/2 transform -translate-x-1/2 hidden sm:block">
        <img 
          src="/logo.png" 
          alt="Logo" 
          class="h-8 w-auto"
        />
      </div>

      <!-- Кнопка авторизации/профиль -->
      <div>
        <template v-if="isAuthenticated">
          <button 
            class="p-2 rounded-full text-white hover:bg-custom-yellow transition-colors"
            aria-label="Профиль"
          >
            <svg 
              class="w-6 h-6" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="2" 
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
          </button>
        </template>
        <template v-else>
          <CustomButton @click="openAuth">
            Авторизация
          </CustomButton>
        </template>
      </div>
    </div>
  </nav>
  <LoginDialog ref="loginDialog" class="mx-4" />
</template>

<script lang="ts" setup>
const visible = ref(false)
const isAuthenticated = ref(false) // Здесь будет ваша логика аутентификации
const loginDialog = ref()

const openAuth = () => {
  loginDialog.value.show()
}
</script>

<style>
.p-drawer {
  background: rgba(0, 0, 0, 0.75) !important;
}

.p-drawer .p-drawer-content {
  background: rgba(0, 0, 0, 0.75) !important;
}
</style>
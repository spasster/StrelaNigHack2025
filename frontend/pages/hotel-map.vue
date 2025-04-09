<!-- pages/hotel-map.vue -->
<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold text-center mb-8 text-white">Выберите номер</h1>
    
    <div class="flex flex-col lg:flex-row gap-8">
      <!-- Легенда и управление -->
      <div class="bg-custom-card p-4 rounded-lg shadow-lg w-full lg:w-64">
        <h2 class="text-lg font-semibold text-white mb-4">Легенда</h2>
        <div class="space-y-2">
          <div class="flex items-center">
            <div class="w-4 h-4 bg-[#e0f7fa] mr-2 rounded"></div>
            <span class="text-white/80">Свободно</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-[#ffcdd2] mr-2 rounded"></div>
            <span class="text-white/80">Занято</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-[#c8e6c9] mr-2 rounded"></div>
            <span class="text-white/80">Выбрано</span>
          </div>
        </div>

        <!-- Выбор этажа -->
        <div class="mt-6">
          <h3 class="text-lg font-semibold text-white mb-2">Этаж</h3>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="floor in floors"
              :key="floor"
              @click="currentFloor = floor"
              :class="[
                'px-3 py-1 rounded transition-colors',
                currentFloor === floor
                  ? 'bg-primary text-white'
                  : 'bg-gray-700 text-white/80 hover:bg-gray-600'
              ]"
            >
              {{ floor }} этаж
            </button>
          </div>
        </div>

        <!-- Информация о выбранном номере -->
        <div v-if="selectedRoom" class="mt-6">
          <h3 class="text-lg font-semibold text-white mb-2">Выбранный номер</h3>
          <div class="bg-gray-700 rounded-lg p-3">
            <p class="text-white">Номер: {{ selectedRoom.number }}</p>
            <p class="text-white">Этаж: {{ currentFloor }}</p>
            <p class="text-white">Тип: {{ getRoomTypeName(selectedRoom.type) }}</p>
            <p class="text-white">Цена: {{ selectedRoom.price }} ₽/сутки</p>
          </div>
          <CustomButton class="w-full mt-3" @click="handleBooking">
            Забронировать
          </CustomButton>
        </div>
      </div>

      <!-- Карта -->
      <div class="flex-1 overflow-auto relative">
        <div class="absolute top-4 left-4 z-50 flex gap-2">
          <button
            @click="handleZoomIn"
            class="bg-gray-700 text-white p-2 rounded-lg hover:bg-gray-600"
          >
            <i class="pi pi-plus"></i>
          </button>
          <button
            @click="handleZoomOut"
            class="bg-gray-700 text-white p-2 rounded-lg hover:bg-gray-600"
          >
            <i class="pi pi-minus"></i>
          </button>
          <button
            @click="handleResetZoom"
            class="bg-gray-700 text-white p-2 rounded-lg hover:bg-gray-600"
          >
            <i class="pi pi-refresh"></i>
          </button>
        </div>
        <div class="relative" :style="{ height: 'calc(100vh - 200px)' }">
          <ClientOnly>
            <v-stage 
              :config="{
                ...stageConfig,
                scale: {
                  x: stageConfig.transform.scale,
                  y: stageConfig.transform.scale
                },
                x: stageConfig.transform.x,
                y: stageConfig.transform.y
              }" 
              class="bg-custom-card rounded-lg p-4 touch-manipulation"
              @wheel="handleZoom"
              @touchstart="handleTouchStart"
              @touchmove="handleTouchMove"
              @touchend="handleTouchEnd"
            >
              <v-layer>
                <!-- Фон здания -->
                <v-rect
                  :config="{
                    x: 0,
                    y: 0,
                    width: stageConfig.width,
                    height: stageConfig.height,
                    fill: '#2d3748',
                    stroke: '#4a5568',
                    strokeWidth: 2,
                  }"
                />

                <!-- Центральный коридор -->
                <v-rect
                  :config="{
                    x: LAYOUT.MARGIN + LAYOUT.SERVICE_ROOM_WIDTH + LAYOUT.MARGIN,
                    y: LAYOUT.MARGIN + LAYOUT.ROOM_HEIGHT + LAYOUT.MARGIN,
                    width: corridorWidth,
                    height: LAYOUT.CORRIDOR_WIDTH,
                    fill: '#4a5568',
                    stroke: '#718096',
                    strokeWidth: 1,
                  }"
                />

                <!-- Лестница (левая) -->
                <v-rect
                  :config="{
                    x: LAYOUT.MARGIN,
                    y: LAYOUT.MARGIN,
                    width: LAYOUT.SERVICE_ROOM_WIDTH,
                    height: LAYOUT.FLOOR_HEIGHT,
                    fill: '#718096',
                    stroke: '#a0aec0',
                    strokeWidth: 2,
                  }"
                />
                <v-text
                  :config="{
                    x: LAYOUT.MARGIN + 5,
                    y: LAYOUT.MARGIN + 20,
                    text: 'Л',
                    fontSize: 16,
                    fill: '#fff',
                    fontStyle: 'bold',
                  }"
                />
                <v-text
                  :config="{
                    x: LAYOUT.MARGIN + 5,
                    y: LAYOUT.MARGIN + 40,
                    text: 'Е',
                    fontSize: 16,
                    fill: '#fff',
                    fontStyle: 'bold',
                  }"
                />
                <v-text
                  :config="{
                    x: LAYOUT.MARGIN + 5,
                    y: LAYOUT.MARGIN + 60,
                    text: 'С',
                    fontSize: 16,
                    fill: '#fff',
                    fontStyle: 'bold',
                  }"
                />
                <v-text
                  :config="{
                    x: LAYOUT.MARGIN + 5,
                    y: LAYOUT.MARGIN + 80,
                    text: 'Т',
                    fontSize: 16,
                    fill: '#fff',
                    fontStyle: 'bold',
                  }"
                />
                <v-text
                  :config="{
                    x: LAYOUT.MARGIN + 5,
                    y: LAYOUT.MARGIN + 100,
                    text: 'Н',
                    fontSize: 16,
                    fill: '#fff',
                    fontStyle: 'bold',
                  }"
                />
                <v-text
                  :config="{
                    x: LAYOUT.MARGIN + 5,
                    y: LAYOUT.MARGIN + 120,
                    text: 'И',
                    fontSize: 16,
                    fill: '#fff',
                    fontStyle: 'bold',
                  }"
                />
                <v-text
                  :config="{
                    x: LAYOUT.MARGIN + 5,
                    y: LAYOUT.MARGIN + 140,
                    text: 'Ц',
                    fontSize: 16,
                    fill: '#fff',
                    fontStyle: 'bold',
                  }"
                />
                <v-text
                  :config="{
                    x: LAYOUT.MARGIN + 5,
                    y: LAYOUT.MARGIN + 160,
                    text: 'А',
                    fontSize: 16,
                    fill: '#fff',
                    fontStyle: 'bold',
                  }"
                />

                <!-- Лестница (правая) -->
                <v-rect
                  :config="{
                    x: stageConfig.width - LAYOUT.MARGIN - LAYOUT.SERVICE_ROOM_WIDTH,
                    y: LAYOUT.MARGIN,
                    width: LAYOUT.SERVICE_ROOM_WIDTH,
                    height: LAYOUT.FLOOR_HEIGHT,
                    fill: '#718096',
                    stroke: '#a0aec0',
                    strokeWidth: 2,
                  }"
                />
                <v-text
                  :config="{
                    x: stageConfig.width - LAYOUT.MARGIN - LAYOUT.SERVICE_ROOM_WIDTH + 5,
                    y: LAYOUT.MARGIN + 20,
                    text: 'Л',
                    fontSize: 16,
                    fill: '#fff',
                    fontStyle: 'bold',
                  }"
                />
                <v-text
                  :config="{
                    x: stageConfig.width - LAYOUT.MARGIN - LAYOUT.SERVICE_ROOM_WIDTH + 5,
                    y: LAYOUT.MARGIN + 40,
                    text: 'Е',
                    fontSize: 16,
                    fill: '#fff',
                    fontStyle: 'bold',
                  }"
                />
                <v-text
                  :config="{
                    x: stageConfig.width - LAYOUT.MARGIN - LAYOUT.SERVICE_ROOM_WIDTH + 5,
                    y: LAYOUT.MARGIN + 60,
                    text: 'С',
                    fontSize: 16,
                    fill: '#fff',
                    fontStyle: 'bold',
                  }"
                />
                <v-text
                  :config="{
                    x: stageConfig.width - LAYOUT.MARGIN - LAYOUT.SERVICE_ROOM_WIDTH + 5,
                    y: LAYOUT.MARGIN + 80,
                    text: 'Т',
                    fontSize: 16,
                    fill: '#fff',
                    fontStyle: 'bold',
                  }"
                />
                <v-text
                  :config="{
                    x: stageConfig.width - LAYOUT.MARGIN - LAYOUT.SERVICE_ROOM_WIDTH + 5,
                    y: LAYOUT.MARGIN + 100,
                    text: 'Н',
                    fontSize: 16,
                    fill: '#fff',
                    fontStyle: 'bold',
                  }"
                />
                <v-text
                  :config="{
                    x: stageConfig.width - LAYOUT.MARGIN - LAYOUT.SERVICE_ROOM_WIDTH + 5,
                    y: LAYOUT.MARGIN + 120,
                    text: 'И',
                    fontSize: 16,
                    fill: '#fff',
                    fontStyle: 'bold',
                  }"
                />
                <v-text
                  :config="{
                    x: stageConfig.width - LAYOUT.MARGIN - LAYOUT.SERVICE_ROOM_WIDTH + 5,
                    y: LAYOUT.MARGIN + 140,
                    text: 'Ц',
                    fontSize: 16,
                    fill: '#fff',
                    fontStyle: 'bold',
                  }"
                />
                <v-text
                  :config="{
                    x: stageConfig.width - LAYOUT.MARGIN - LAYOUT.SERVICE_ROOM_WIDTH + 5,
                    y: LAYOUT.MARGIN + 160,
                    text: 'А',
                    fontSize: 16,
                    fill: '#fff',
                    fontStyle: 'bold',
                  }"
                />

                <!-- Служебные помещения в центре коридора -->
                <v-rect
                  :config="{
                    x: LAYOUT.MARGIN + LAYOUT.SERVICE_ROOM_WIDTH + LAYOUT.MARGIN + (corridorWidth / 2 - LAYOUT.SERVICE_ROOM_WIDTH * 1.5 - LAYOUT.SERVICE_ROOMS_SPACING),
                    y: LAYOUT.MARGIN + LAYOUT.ROOM_HEIGHT + LAYOUT.MARGIN + LAYOUT.CORRIDOR_WIDTH / 2 - LAYOUT.COOLER_HEIGHT / 2,
                    width: LAYOUT.COOLER_WIDTH,
                    height: LAYOUT.COOLER_HEIGHT,
                    fill: '#4299e1',
                    stroke: '#63b3ed',
                    strokeWidth: 1,
                  }"
                />
                <v-text
                  :config="{
                    x: LAYOUT.MARGIN + LAYOUT.SERVICE_ROOM_WIDTH + LAYOUT.MARGIN + (corridorWidth / 2 - LAYOUT.SERVICE_ROOM_WIDTH * 1.5 - LAYOUT.SERVICE_ROOMS_SPACING) + 5,
                    y: LAYOUT.MARGIN + LAYOUT.ROOM_HEIGHT + LAYOUT.MARGIN + LAYOUT.CORRIDOR_WIDTH / 2 - 5,
                    text: 'Кулер',
                    fontSize: 12,
                    fill: '#fff',
                  }"
                />

                <v-rect
                  :config="{
                    x: LAYOUT.MARGIN + LAYOUT.SERVICE_ROOM_WIDTH + LAYOUT.MARGIN + (corridorWidth / 2 - LAYOUT.SERVICE_ROOM_WIDTH / 2),
                    y: LAYOUT.MARGIN + LAYOUT.ROOM_HEIGHT + LAYOUT.MARGIN + LAYOUT.CORRIDOR_WIDTH / 2 - LAYOUT.SERVICE_ROOM_HEIGHT / 2,
                    width: LAYOUT.SERVICE_ROOM_WIDTH,
                    height: LAYOUT.SERVICE_ROOM_HEIGHT,
                    fill: '#718096',
                    stroke: '#a0aec0',
                    strokeWidth: 2,
                  }"
                />
                <v-text
                  :config="{
                    x: LAYOUT.MARGIN + LAYOUT.SERVICE_ROOM_WIDTH + LAYOUT.MARGIN + (corridorWidth / 2 - LAYOUT.SERVICE_ROOM_WIDTH / 2) + 5,
                    y: LAYOUT.MARGIN + LAYOUT.ROOM_HEIGHT + LAYOUT.MARGIN + LAYOUT.CORRIDOR_WIDTH / 2 - 5,
                    text: 'Лифт',
                    fontSize: 12,
                    fill: '#fff',
                    fontStyle: 'bold',
                  }"
                />

                <v-rect
                  :config="{
                    x: LAYOUT.MARGIN + LAYOUT.SERVICE_ROOM_WIDTH + LAYOUT.MARGIN + (corridorWidth / 2 + LAYOUT.SERVICE_ROOMS_SPACING),
                    y: LAYOUT.MARGIN + LAYOUT.ROOM_HEIGHT + LAYOUT.MARGIN + LAYOUT.CORRIDOR_WIDTH / 2 - LAYOUT.SERVICE_ROOM_HEIGHT / 2,
                    width: LAYOUT.SERVICE_ROOM_WIDTH,
                    height: LAYOUT.SERVICE_ROOM_HEIGHT,
                    fill: '#805ad5',
                    stroke: '#9f7aea',
                    strokeWidth: 1,
                  }"
                />
                <v-text
                  :config="{
                    x: LAYOUT.MARGIN + LAYOUT.SERVICE_ROOM_WIDTH + LAYOUT.MARGIN + (corridorWidth / 2 + LAYOUT.SERVICE_ROOMS_SPACING) + 5,
                    y: LAYOUT.MARGIN + LAYOUT.ROOM_HEIGHT + LAYOUT.MARGIN + LAYOUT.CORRIDOR_WIDTH / 2 - 5,
                    text: 'WC',
                    fontSize: 12,
                    fill: '#fff',
                    fontStyle: 'bold',
                  }"
                />
                
                <!-- Номера -->
                <v-rect
                  v-for="room in currentFloorRooms"
                  :key="room.number"
                  :config="{
                    x: room.x,
                    y: room.y,
                    width: LAYOUT.ROOM_WIDTH,
                    height: LAYOUT.ROOM_HEIGHT,
                    fill: room.fill,
                    stroke: '#4a5568',
                    strokeWidth: 2,
                    cornerRadius: 4,
                  }"
                  @click="handleRoomClick(room)"
                  @mouseover="handleRoomHover(room)"
                  @mouseout="handleRoomHoverOut(room)"
                />
                
                <!-- Номера комнат -->
                <v-text
                  v-for="room in currentFloorRooms"
                  :key="'text-' + room.number"
                  :config="{
                    x: room.x + LAYOUT.ROOM_WIDTH / 2 - 15,
                    y: room.y + LAYOUT.ROOM_HEIGHT / 2 - 10,
                    text: room.number,
                    fontSize: 18,
                    fill: '#2d3748',
                    fontStyle: 'bold',
                  }"
                />

                <!-- Статус комнат -->
                <v-text
                  v-for="room in currentFloorRooms"
                  :key="'status-' + room.number"
                  :config="{
                    x: room.x + 5,
                    y: room.y + 5,
                    text: getStatusText(room.status),
                    fontSize: 12,
                    fill: '#2d3748',
                  }"
                />

                <!-- Входы/выходы (только на первом этаже) -->
                <template v-if="currentFloor === 1">
                  <!-- Вход между верхними номерами -->
                  <v-rect
                    :config="{
                      x: LAYOUT.MARGIN + LAYOUT.SERVICE_ROOM_WIDTH + LAYOUT.MARGIN + corridorWidth / 2 - LAYOUT.ENTRANCE_WIDTH / 2 - 35,
                      y: LAYOUT.MARGIN + LAYOUT.ROOM_HEIGHT / 2 - LAYOUT.ENTRANCE_HEIGHT / 2,
                      width: LAYOUT.ENTRANCE_WIDTH,
                      height: LAYOUT.ENTRANCE_HEIGHT,
                      fill: '#4a5568',
                      stroke: '#718096',
                      strokeWidth: 1,
                    }"
                  />
                  <v-text
                    :config="{
                      x: LAYOUT.MARGIN + LAYOUT.SERVICE_ROOM_WIDTH + LAYOUT.MARGIN + corridorWidth / 2 - LAYOUT.ENTRANCE_WIDTH / 2 + 5 - 35,
                      y: LAYOUT.MARGIN + LAYOUT.ROOM_HEIGHT / 2 - 5,
                      text: 'Вход',
                      fontSize: 12,
                      fill: '#fff',
                      fontStyle: 'bold',
                    }"
                  />

                  <!-- Выход между нижними номерами -->
                  <v-rect
                    :config="{
                      x: LAYOUT.MARGIN + LAYOUT.SERVICE_ROOM_WIDTH + LAYOUT.MARGIN + corridorWidth / 2 - LAYOUT.ENTRANCE_WIDTH / 2 - 35,
                      y: LAYOUT.MARGIN + LAYOUT.ROOM_HEIGHT + LAYOUT.MARGIN * 2 + LAYOUT.CORRIDOR_WIDTH + LAYOUT.ROOM_HEIGHT / 2 - LAYOUT.ENTRANCE_HEIGHT / 2,
                      width: LAYOUT.ENTRANCE_WIDTH,
                      height: LAYOUT.ENTRANCE_HEIGHT,
                      fill: '#4a5568',
                      stroke: '#718096',
                      strokeWidth: 1,
                    }"
                  />
                  <v-text
                    :config="{
                      x: LAYOUT.MARGIN + LAYOUT.SERVICE_ROOM_WIDTH + LAYOUT.MARGIN + corridorWidth / 2 - LAYOUT.ENTRANCE_WIDTH / 2 + 5 - 35,
                      y: LAYOUT.MARGIN + LAYOUT.ROOM_HEIGHT + LAYOUT.MARGIN * 2 + LAYOUT.CORRIDOR_WIDTH + LAYOUT.ROOM_HEIGHT / 2 - 5,
                      text: 'Выход',
                      fontSize: 12,
                      fill: '#fff',
                      fontStyle: 'bold',
                    }"
                  />
                </template>
              </v-layer>
            </v-stage>
          </ClientOnly>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useToast } from 'primevue/usetoast';

// Типы для интеграции с бэкендом
interface Room {
  id: number;
  number: string;
  floor: number;
  type: RoomType;
  status: RoomStatus;
  price: number;
  x: number;
  y: number;
  fill: string;
  capacity: number;
  description: string;
  amenities: string[];
  images: string[];
}

type RoomType = 'standard' | 'luxury' | 'suite';
type RoomStatus = 'free' | 'booked' | 'selected' | 'maintenance';

const toast = useToast();

const stageConfig = reactive({
  width: 1400,
  height: 900,
  scale: 1,
  draggable: true,
  lastTouchX: 0,
  lastTouchY: 0,
  lastDistance: 0 as number | null,
  x: 0,
  y: 0,
  transform: {
    scale: 1,
    x: 0,
    y: 0
  },
  // Добавляем новые параметры для мобильного масштабирования
  minScale: 0.3,
  maxScale: 5,
  scaleStep: 1.1,
  isMobile: false
});

const floors = [1, 2, 3, 4, 5];
const currentFloor = ref(1);
const selectedRoom = ref<Room | null>(null);

// Константы для планировки
const LAYOUT = {
  ROOM_WIDTH: 120,
  ROOM_HEIGHT: 100,
  CORRIDOR_WIDTH: 120,
  SERVICE_ROOM_WIDTH: 100,
  SERVICE_ROOM_HEIGHT: 100,
  COOLER_WIDTH: 60,
  COOLER_HEIGHT: 60,
  MARGIN: 40,
  FLOOR_HEIGHT: 800,
  ROOMS_PER_SIDE: 3,
  ROOMS_PER_FLOOR: 12,
  SERVICE_ROOMS_SPACING: 60,
  ROOM_SPACING: 30,
  ENTRANCE_WIDTH: 80,
  ENTRANCE_HEIGHT: 30,
};

// Вычисляем ширину коридора
const corridorWidth = computed(() => {
  return stageConfig.width - (LAYOUT.MARGIN * 2 + LAYOUT.SERVICE_ROOM_WIDTH * 2 + LAYOUT.MARGIN * 2);
});

// Функция для создания комнат
const createFloorRooms = (floor: number): Room[] => {
  const rooms: Room[] = [];
  const startX = LAYOUT.MARGIN + LAYOUT.SERVICE_ROOM_WIDTH + LAYOUT.MARGIN;
  const startY = LAYOUT.MARGIN;
  const corridorY = startY + LAYOUT.ROOM_HEIGHT + LAYOUT.MARGIN;
  const corridorWidthValue = corridorWidth.value;
  
  // Верхний ряд (левая сторона)
  for (let i = 0; i < LAYOUT.ROOMS_PER_SIDE; i++) {
    const x = startX + i * (LAYOUT.ROOM_WIDTH + LAYOUT.ROOM_SPACING);
    const type = i === 0 ? 'suite' : i === LAYOUT.ROOMS_PER_SIDE - 1 ? 'luxury' : 'standard';
    const price = type === 'luxury' ? 5000 : type === 'suite' ? 8000 : 3000;
    const status = Math.random() > 0.7 ? 'booked' : 'free';
    rooms.push({
      id: floor * 100 + i + 1,
      number: `${floor}${(i + 1).toString().padStart(2, '0')}`,
      floor,
      type,
      status,
      price,
      x,
      y: startY,
      fill: status === 'booked' ? '#ffcdd2' : '#e0f7fa',
      capacity: type === 'luxury' ? 3 : type === 'suite' ? 4 : 2,
      description: `${type === 'luxury' ? 'Люксовый' : type === 'suite' ? 'Сьют' : 'Стандартный'} номер`,
      amenities: ['Wi-Fi', 'TV', 'Кондиционер', type === 'luxury' ? 'Мини-бар' : type === 'suite' ? 'Джакузи' : ''],
      images: [],
    });
  }

  // Верхний ряд (правая сторона)
  for (let i = 0; i < LAYOUT.ROOMS_PER_SIDE; i++) {
    const x = startX + corridorWidthValue / 2 + LAYOUT.ROOM_SPACING + i * (LAYOUT.ROOM_WIDTH + LAYOUT.ROOM_SPACING);
    const type = i === 0 ? 'suite' : i === LAYOUT.ROOMS_PER_SIDE - 1 ? 'luxury' : 'standard';
    const price = type === 'luxury' ? 5000 : type === 'suite' ? 8000 : 3000;
    const status = Math.random() > 0.7 ? 'booked' : 'free';
    rooms.push({
      id: floor * 100 + i + LAYOUT.ROOMS_PER_SIDE + 1,
      number: `${floor}${(i + LAYOUT.ROOMS_PER_SIDE + 1).toString().padStart(2, '0')}`,
      floor,
      type,
      status,
      price,
      x,
      y: startY,
      fill: status === 'booked' ? '#ffcdd2' : '#e0f7fa',
      capacity: type === 'luxury' ? 3 : type === 'suite' ? 4 : 2,
      description: `${type === 'luxury' ? 'Люксовый' : type === 'suite' ? 'Сьют' : 'Стандартный'} номер`,
      amenities: ['Wi-Fi', 'TV', 'Кондиционер', type === 'luxury' ? 'Мини-бар' : type === 'suite' ? 'Джакузи' : ''],
      images: [],
    });
  }

  // Нижний ряд (левая сторона)
  for (let i = 0; i < LAYOUT.ROOMS_PER_SIDE; i++) {
    const x = startX + i * (LAYOUT.ROOM_WIDTH + LAYOUT.ROOM_SPACING);
    const type = i === 0 ? 'suite' : i === LAYOUT.ROOMS_PER_SIDE - 1 ? 'luxury' : 'standard';
    const price = type === 'luxury' ? 5000 : type === 'suite' ? 8000 : 3000;
    const status = Math.random() > 0.7 ? 'booked' : 'free';
    rooms.push({
      id: floor * 100 + i + LAYOUT.ROOMS_PER_SIDE * 2 + 1,
      number: `${floor}${(i + LAYOUT.ROOMS_PER_SIDE * 2 + 1).toString().padStart(2, '0')}`,
      floor,
      type,
      status,
      price,
      x,
      y: corridorY + LAYOUT.CORRIDOR_WIDTH + LAYOUT.MARGIN,
      fill: status === 'booked' ? '#ffcdd2' : '#e0f7fa',
      capacity: type === 'luxury' ? 3 : type === 'suite' ? 4 : 2,
      description: `${type === 'luxury' ? 'Люксовый' : type === 'suite' ? 'Сьют' : 'Стандартный'} номер`,
      amenities: ['Wi-Fi', 'TV', 'Кондиционер', type === 'luxury' ? 'Мини-бар' : type === 'suite' ? 'Джакузи' : ''],
      images: [],
    });
  }

  // Нижний ряд (правая сторона)
  for (let i = 0; i < LAYOUT.ROOMS_PER_SIDE; i++) {
    const x = startX + corridorWidthValue / 2 + LAYOUT.ROOM_SPACING + i * (LAYOUT.ROOM_WIDTH + LAYOUT.ROOM_SPACING);
    const type = i === 0 ? 'suite' : i === LAYOUT.ROOMS_PER_SIDE - 1 ? 'luxury' : 'standard';
    const price = type === 'luxury' ? 5000 : type === 'suite' ? 8000 : 3000;
    const status = Math.random() > 0.7 ? 'booked' : 'free';
    rooms.push({
      id: floor * 100 + i + LAYOUT.ROOMS_PER_SIDE * 3 + 1,
      number: `${floor}${(i + LAYOUT.ROOMS_PER_SIDE * 3 + 1).toString().padStart(2, '0')}`,
      floor,
      type,
      status,
      price,
      x,
      y: corridorY + LAYOUT.CORRIDOR_WIDTH + LAYOUT.MARGIN,
      fill: status === 'booked' ? '#ffcdd2' : '#e0f7fa',
      capacity: type === 'luxury' ? 3 : type === 'suite' ? 4 : 2,
      description: `${type === 'luxury' ? 'Люксовый' : type === 'suite' ? 'Сьют' : 'Стандартный'} номер`,
      amenities: ['Wi-Fi', 'TV', 'Кондиционер', type === 'luxury' ? 'Мини-бар' : type === 'suite' ? 'Джакузи' : ''],
      images: [],
    });
  }

  return rooms;
};

// Создаем данные для всех этажей
const rooms = ref<Record<number, Room[]>>({
  1: createFloorRooms(1),
  2: createFloorRooms(2),
  3: createFloorRooms(3),
  4: createFloorRooms(4),
  5: createFloorRooms(5),
});

const currentFloorRooms = computed(() => rooms.value[currentFloor.value] || []);

const getStatusText = (status: RoomStatus): string => {
  switch (status) {
    case 'free':
      return 'Свободно';
    case 'booked':
      return 'Занято';
    case 'selected':
      return 'Выбрано';
    case 'maintenance':
      return 'В ремонте';
    default:
      return '';
  }
};

const getRoomTypeName = (type: RoomType): string => {
  return type === 'luxury' ? 'Люкс' : type === 'suite' ? 'Сьют' : 'Стандарт';
};

const handleRoomClick = (room: Room) => {
  if (room.status === 'free') {
    // Сбрасываем предыдущий выбор
    Object.values(rooms.value).forEach(floorRooms => {
      floorRooms.forEach(r => {
        if (r.status === 'selected') {
          r.status = 'free';
          r.fill = '#e0f7fa';
        }
      });
    });
    
    // Выбираем новую комнату
    room.status = 'selected';
    room.fill = '#c8e6c9';
    selectedRoom.value = room;
  }
};

const handleRoomHover = (room: Room) => {
  if (room.status === 'free') {
    room.fill = '#b2ebf2';
  }
};

const handleRoomHoverOut = (room: Room) => {
  if (room.status === 'free') {
    room.fill = '#e0f7fa';
  }
};

const handleZoom = (e: WheelEvent) => {
  if (e.cancelable) {
    e.preventDefault();
  }
  
  const scaleBy = stageConfig.scaleStep;
  const oldScale = stageConfig.transform.scale;
  
  // Получаем позицию курсора относительно сцены
  const stage = e.target as HTMLElement;
  const rect = stage.getBoundingClientRect();
  const pointer = {
    x: e.clientX - rect.left,
    y: e.clientY - rect.top
  };
  
  // Вычисляем новый масштаб
  const newScale = e.deltaY > 0 ? oldScale / scaleBy : oldScale * scaleBy;
  const clampedScale = Math.max(stageConfig.minScale, Math.min(stageConfig.maxScale, newScale));
  
  // Вычисляем точку относительно текущего масштаба
  const mousePointTo = {
    x: (pointer.x - stageConfig.transform.x) / oldScale,
    y: (pointer.y - stageConfig.transform.y) / oldScale
  };
  
  // Вычисляем новую позицию
  const newPos = {
    x: pointer.x - mousePointTo.x * clampedScale,
    y: pointer.y - mousePointTo.y * clampedScale
  };
  
  // Обновляем состояние
  stageConfig.transform.scale = clampedScale;
  stageConfig.transform.x = newPos.x;
  stageConfig.transform.y = newPos.y;
};

const handleBooking = async () => {
  if (!selectedRoom.value) return;

  try {
    // Здесь будет запрос к API для бронирования
    const response = await fetch('/api/booking/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        roomId: selectedRoom.value.id,
        // Другие данные для бронирования
      }),
    });

    if (response.ok) {
      toast.add({
        severity: 'success',
        summary: 'Успех',
        detail: 'Номер успешно забронирован',
        life: 3000,
      });
      // Обновляем статус комнаты
      selectedRoom.value.status = 'booked';
      selectedRoom.value.fill = '#ffcdd2';
      selectedRoom.value = null;
    } else {
      throw new Error('Ошибка при бронировании');
    }
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось забронировать номер',
      life: 3000,
    });
  }
};

// Функция для загрузки данных с бэкенда
const fetchRooms = async () => {
  try {
    const response = await fetch('/api/rooms');
    if (!response.ok) throw new Error('Ошибка загрузки данных');
    const data = await response.json();
    rooms.value = data;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось загрузить данные о номерах',
      life: 3000,
    });
  }
};

// Обновляем обработчики тач-событий
const handleTouchStart = (e: TouchEvent) => {
  // Предотвращаем стандартное поведение для всех тач-событий
  e.preventDefault();
  
  if (e.touches.length === 1) {
    const touch = e.touches[0];
    const stage = e.target as HTMLElement;
    const rect = stage.getBoundingClientRect();
    const x = touch.clientX - rect.left;
    const y = touch.clientY - rect.top;
    
    stageConfig.lastTouchX = x;
    stageConfig.lastTouchY = y;
  } else if (e.touches.length === 2) {
    const touch1 = e.touches[0];
    const touch2 = e.touches[1];
    stageConfig.lastDistance = Math.hypot(
      touch2.clientX - touch1.clientX,
      touch2.clientY - touch1.clientY
    );
  }
};

const handleTouchMove = (e: TouchEvent) => {
  // Предотвращаем стандартное поведение для всех тач-событий
  e.preventDefault();
  
  if (e.touches.length === 1) {
    const touch = e.touches[0];
    const stage = e.target as HTMLElement;
    const rect = stage.getBoundingClientRect();
    const x = touch.clientX - rect.left;
    const y = touch.clientY - rect.top;
    
    const dx = x - stageConfig.lastTouchX;
    const dy = y - stageConfig.lastTouchY;
    
    stageConfig.transform.x += dx;
    stageConfig.transform.y += dy;
    
    stageConfig.lastTouchX = x;
    stageConfig.lastTouchY = y;
  } else if (e.touches.length === 2) {
    const touch1 = e.touches[0];
    const touch2 = e.touches[1];
    const distance = Math.hypot(
      touch2.clientX - touch1.clientX,
      touch2.clientY - touch1.clientY
    );
    
    if (stageConfig.lastDistance) {
      const scale = distance / stageConfig.lastDistance;
      const newScale = stageConfig.transform.scale * scale;
      stageConfig.transform.scale = Math.max(stageConfig.minScale, Math.min(stageConfig.maxScale, newScale));
    }
    
    stageConfig.lastDistance = distance;
  }
};

const handleTouchEnd = () => {
  stageConfig.lastDistance = null;
};

// Обновляем mounted
onMounted(() => {
  stageConfig.isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  if (stageConfig.isMobile) {
    stageConfig.minScale = 0.2;
    stageConfig.maxScale = 6;
    stageConfig.scaleStep = 1.05;
    
    // Добавляем обработчики для предотвращения стандартного масштабирования
    document.addEventListener('gesturestart', (e) => e.preventDefault(), { passive: false });
    document.addEventListener('gesturechange', (e) => e.preventDefault(), { passive: false });
    document.addEventListener('gestureend', (e) => e.preventDefault(), { passive: false });
    
    // Добавляем мета-тег для предотвращения масштабирования страницы
    const meta = document.createElement('meta');
    meta.name = 'viewport';
    meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
    document.head.appendChild(meta);
  }
  fetchRooms();
});

// Обновляем unmounted
onUnmounted(() => {
  if (stageConfig.isMobile) {
    document.removeEventListener('gesturestart', (e) => e.preventDefault());
    document.removeEventListener('gesturechange', (e) => e.preventDefault());
    document.removeEventListener('gestureend', (e) => e.preventDefault());
  }
});

// Обновляем функции управления масштабом
const handleZoomIn = () => {
  const newScale = Math.min(stageConfig.maxScale, stageConfig.transform.scale * stageConfig.scaleStep);
  stageConfig.transform.scale = newScale;
};

const handleZoomOut = () => {
  const newScale = Math.max(stageConfig.minScale, stageConfig.transform.scale / stageConfig.scaleStep);
  stageConfig.transform.scale = newScale;
};

const handleResetZoom = () => {
  stageConfig.transform.scale = 1;
  stageConfig.transform.x = 0;
  stageConfig.transform.y = 0;
};
</script>

<style scoped>
.container {
  min-height: calc(100vh - 64px);
  /* background: linear-gradient(to bottom, #1a202c, #2d3748); */
}

.touch-manipulation {
  touch-action: none; /* Отключаем стандартное поведение тач-событий */
  -webkit-overflow-scrolling: touch;
  -webkit-tap-highlight-color: transparent;
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  user-select: none;
  /* Добавляем дополнительные стили для iOS */
  -webkit-text-size-adjust: none;
  text-size-adjust: none;
  -webkit-user-drag: none;
  -webkit-touch-callout: none;
}

@media (max-width: 1024px) {
  .container {
    padding: 1rem;
    touch-action: none; /* Отключаем стандартное поведение тач-событий */
    -webkit-text-size-adjust: none;
    text-size-adjust: none;
    overflow: hidden; /* Предотвращаем прокрутку страницы */
  }
  
  .v-stage {
    transform-origin: 0 0;
    will-change: transform;
    backface-visibility: hidden;
    perspective: 1000;
    transform-style: preserve-3d;
    transition: transform 0.1s ease-out;
  }
}
</style>
from django.urls import path
from .views import (
    RoomCreateView,
    RoomListView,
    RoomDetailView,
    CheckInInformationCreateView,
    FurnitureCreateView,
    FurnitureListView,
    FurnitureMoveView,
    FurnitureDeleteView
)

urlpatterns = [
    path('create/', RoomCreateView.as_view(), name='room-create'),
    path('list/', RoomListView.as_view(), name='room-list'),
    path('detail/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('check-in/', CheckInInformationCreateView.as_view(), name='check-in'),
    path('furniture/create/', FurnitureCreateView.as_view(), name='furniture-create'),
    path('furniture/room/<int:room_id>/', FurnitureListView.as_view(), name='furniture-list'),
    path('furniture/<int:pk>/move/', FurnitureMoveView.as_view(), name='furniture-move'),
    path('furniture/<int:pk>/delete/', FurnitureDeleteView.as_view(), name='furniture-delete'),
] 
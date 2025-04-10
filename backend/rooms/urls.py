from django.urls import path
from .views import (
    RoomCreateView,
    RoomListView,
    RoomDetailView,
    CheckInInformationCreateView,
    FurnitureCreateView,
    FurnitureListView,
    FurnitureMoveView,
    FurnitureDeleteView,
    UserCheckInInfoView,
    AllFurnitureListView,
    OccupancyReportView,
    UniversityReportView,
    CheckInReportView,
    ExportReportView,
    CheckInInformationWithoutRoomAndEmailCreateView,
    AllCheckInInformationListView,
    CheckInInformationAssignView,
    CheckInInformationUnassignView
)
from . import views

urlpatterns = [
    path('create/', RoomCreateView.as_view(), name='room-create'),
    path('list/', RoomListView.as_view(), name='room-list'),
    path('detail/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('check-in/', CheckInInformationCreateView.as_view(), name='check-in'),
    path('furniture/create/', FurnitureCreateView.as_view(), name='furniture-create'),
    path('furniture/room/<int:room_id>/', FurnitureListView.as_view(), name='furniture-list'),
    path('furniture/<int:pk>/move/', FurnitureMoveView.as_view(), name='furniture-move'),
    path('furniture/<int:pk>/delete/', FurnitureDeleteView.as_view(), name='furniture-delete'),
    path('my-check-in/', UserCheckInInfoView.as_view(), name='user-check-in-info'),
    path('furniture/all/', AllFurnitureListView.as_view(), name='all-furniture'),
    path('reports/occupancy/', OccupancyReportView.as_view(), name='occupancy-report'),
    path('reports/university/', UniversityReportView.as_view(), name='university-report'),
    path('reports/checkin/', CheckInReportView.as_view(), name='checkin-report'),
    path('reports/export/', ExportReportView.as_view(), name='export-report'),
    path('check-in/without-room-and-email/', CheckInInformationWithoutRoomAndEmailCreateView.as_view(), name='check-in-without-room-and-email'),
    path('check-in/all/', AllCheckInInformationListView.as_view(), name='all-check-ins'),
    path('check-in/assign/', CheckInInformationAssignView.as_view(), name='check-in-assign'),
    path('check-in/unassign/', CheckInInformationUnassignView.as_view(), name='check-in-unassign'),
    path('check-in/create-with-bill/', views.CreateCheckInWithBillView.as_view(), name='create-check-in-with-bill'),
] 
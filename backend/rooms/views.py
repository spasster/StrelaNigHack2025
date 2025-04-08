from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Room, CheckInInformation, Furniture
from .serializers import (
    RoomSerializer, 
    CheckInInformationSerializer,
    FurnitureSerializer
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class RoomCreateView(generics.CreateAPIView):
    """
    Создание новой комнаты.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @swagger_auto_schema(
        operation_description="Создание новой комнаты",
        request_body=RoomSerializer,
        responses={
            201: RoomSerializer,
            400: "Неверные данные"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'message': 'Комната успешно создана',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomListView(generics.ListAPIView):
    """
    Получение списка всех комнат.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @swagger_auto_schema(
        operation_description="Получение списка всех комнат",
        responses={200: RoomSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class RoomDetailView(generics.RetrieveAPIView):
    """
    Получение детальной информации о комнате.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @swagger_auto_schema(
        operation_description="Получение детальной информации о комнате",
        responses={200: RoomSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class CheckInInformationCreateView(generics.CreateAPIView):
    """
    Создание информации о заселении.
    """
    queryset = CheckInInformation.objects.all()
    serializer_class = CheckInInformationSerializer

    @swagger_auto_schema(
        operation_description="Создание информации о заселении",
        request_body=CheckInInformationSerializer,
        responses={
            201: CheckInInformationSerializer,
            400: "Неверные данные"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'message': 'Успешное заселение',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FurnitureCreateView(generics.CreateAPIView):
    """
    Создание новой мебели.
    """
    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer

    @swagger_auto_schema(
        operation_description="Создание новой мебели",
        request_body=FurnitureSerializer,
        responses={
            201: FurnitureSerializer,
            400: "Неверные данные"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'message': 'Мебель успешно добавлена',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FurnitureListView(generics.ListAPIView):
    """
    Получение списка мебели в комнате.
    """
    serializer_class = FurnitureSerializer

    @swagger_auto_schema(
        operation_description="Получение списка мебели в комнате",
        manual_parameters=[
            openapi.Parameter(
                'room_id',
                openapi.IN_PATH,
                description="ID комнаты",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={200: FurnitureSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        room_id = self.kwargs.get('room_id')
        return Furniture.objects.filter(room_id=room_id)

class FurnitureMoveView(generics.UpdateAPIView):
    """
    Перемещение мебели в другую комнату.
    """
    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer

    @swagger_auto_schema(
        operation_description="Перемещение мебели в другую комнату",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'room': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID новой комнаты')
            }
        ),
        responses={
            200: FurnitureSerializer,
            404: "Комната не найдена"
        }
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_room_id = request.data.get('room')
        
        try:
            new_room = Room.objects.get(id=new_room_id)
            instance.move_to_room(new_room)
            return Response({
                'message': 'Мебель успешно перемещена',
                'data': self.get_serializer(instance).data
            })
        except Room.DoesNotExist:
            return Response(
                {'error': 'Комната не найдена'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class FurnitureDeleteView(generics.DestroyAPIView):
    """
    Удаление мебели из комнаты.
    """
    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer

    @swagger_auto_schema(
        operation_description="Удаление мебели из комнаты",
        responses={
            200: "Мебель успешно удалена",
            404: "Мебель не найдена"
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.remove_from_room()
        return Response({
            'message': 'Мебель успешно удалена'
        }, status=status.HTTP_200_OK)

class UserCheckInInfoView(generics.RetrieveAPIView):
    """
    Получение информации о заселении текущего пользователя.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CheckInInformationSerializer

    @swagger_auto_schema(
        operation_description="Получение информации о заселении текущего пользователя",
        responses={
            200: CheckInInformationSerializer,
            404: "Информация о заселении не найдена"
        }
    )
    def get(self, request, *args, **kwargs):
        user_email = request.user.email
        check_in_info = CheckInInformation.get_user_info(user_email)
        
        if check_in_info:
            serializer = self.get_serializer(check_in_info)
            return Response(serializer.data)
        return Response(
            {'error': 'Информация о заселении не найдена'}, 
            status=status.HTTP_404_NOT_FOUND
        )

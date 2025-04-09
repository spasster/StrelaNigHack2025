from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Room, CheckInInformation, Furniture
from .serializers import (
    RoomSerializer, 
    CheckInInformationSerializer,
    FurnitureSerializer,
    OccupancyReportSerializer,
    UniversityReportSerializer,
    CheckInReportSerializer,
    CheckInInformationWithoutRoomAndEmailSerializer,
    CheckInInformationAssignSerializer
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Count, F, Q
from datetime import datetime, timedelta
import pandas as pd
from django.http import HttpResponse
import io

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
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Создание информации о заселении",
        request_body=CheckInInformationSerializer,
        responses={
            201: CheckInInformationSerializer,
            400: "Неверные данные"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        # Если email не указан, берем из токена
        if 'email' not in data and request.user.is_authenticated:
            data['email'] = request.user.email
            
        serializer = self.get_serializer(data=data)
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

class AllFurnitureListView(generics.ListAPIView):
    """
    Получение списка всей мебели.
    """
    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получение списка всей мебели",
        responses={200: FurnitureSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class OccupancyReportView(generics.GenericAPIView):
    """
    Генерация отчета по заполняемости комнат.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получение отчета по заполняемости комнат",
        responses={200: OccupancyReportSerializer}
    )
    def get(self, request):
        total_rooms = Room.objects.count()
        occupied_rooms = Room.objects.filter(occupied_seats__gt=0).count()
        free_rooms = total_rooms - occupied_rooms
        occupancy_rate = (occupied_rooms / total_rooms) * 100 if total_rooms > 0 else 0
        
        rooms_by_gender = Room.objects.values('gender').annotate(
            count=Count('id')
        ).values('gender', 'count')
        
        data = {
            'total_rooms': total_rooms,
            'occupied_rooms': occupied_rooms,
            'free_rooms': free_rooms,
            'occupancy_rate': occupancy_rate,
            'rooms_by_gender': {item['gender']: item['count'] for item in rooms_by_gender}
        }
        
        serializer = OccupancyReportSerializer(data)
        return Response(serializer.data)

class UniversityReportView(generics.GenericAPIView):
    """
    Генерация отчета по распределению студентов по вузам, факультетам и курсам.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получение отчета по распределению студентов",
        responses={200: UniversityReportSerializer(many=True)}
    )
    def get(self, request):
        reports = []
        universities = CheckInInformation.objects.values('university').distinct()
        
        for uni in universities:
            university = uni['university']
            students = CheckInInformation.objects.filter(university=university)
            
            faculties = students.values('faculty').annotate(
                count=Count('id')
            ).values('faculty', 'count')
            
            courses = students.values('course').annotate(
                count=Count('id')
            ).values('course', 'count')
            
            data = {
                'university': university,
                'total_students': students.count(),
                'faculties': {item['faculty']: item['count'] for item in faculties},
                'courses': {item['course']: item['count'] for item in courses}
            }
            
            reports.append(data)
        
        serializer = UniversityReportSerializer(reports, many=True)
        return Response(serializer.data)

class CheckInReportView(generics.GenericAPIView):
    """
    Генерация отчета по срокам проживания.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получение отчета по срокам проживания",
        responses={200: CheckInReportSerializer}
    )
    def get(self, request):
        students = CheckInInformation.objects.all()
        total_students = students.count()
        
        # Расчет средней продолжительности проживания
        durations = []
        for student in students:
            if student.check_out_date:
                duration = (student.check_out_date - student.check_in_date).days
                durations.append(duration)
        
        average_stay_duration = sum(durations) / len(durations) if durations else 0
        
        # Группировка по продолжительности проживания
        duration_ranges = {
            'less_than_month': students.filter(
                check_out_date__lte=F('check_in_date') + timedelta(days=30)
            ).count(),
            '1-3_months': students.filter(
                check_out_date__gt=F('check_in_date') + timedelta(days=30),
                check_out_date__lte=F('check_in_date') + timedelta(days=90)
            ).count(),
            '3-6_months': students.filter(
                check_out_date__gt=F('check_in_date') + timedelta(days=90),
                check_out_date__lte=F('check_in_date') + timedelta(days=180)
            ).count(),
            'more_than_6_months': students.filter(
                check_out_date__gt=F('check_in_date') + timedelta(days=180)
            ).count()
        }
        
        data = {
            'total_students': total_students,
            'average_stay_duration': average_stay_duration,
            'students_by_duration': duration_ranges
        }
        
        serializer = CheckInReportSerializer(data)
        return Response(serializer.data)

class ExportReportView(generics.GenericAPIView):
    """
    Экспорт отчетов в Excel.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Экспорт отчетов в Excel",
        manual_parameters=[
            openapi.Parameter(
                'report_type',
                openapi.IN_QUERY,
                description="Тип отчета (occupancy/university/checkin)",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request):
        report_type = request.query_params.get('report_type')
        
        if report_type == 'occupancy':
            # Экспорт отчета по заполняемости
            rooms = Room.objects.all()
            data = []
            for room in rooms:
                data.append({
                    'ID комнаты': room.id,
                    'Всего мест': room.seats,
                    'Занято мест': room.occupied_seats,
                    'Пол': room.gender,
                    'Заполняемость (%)': (room.occupied_seats / room.seats) * 100
                })
            
        elif report_type == 'university':
            # Экспорт отчета по вузам
            students = CheckInInformation.objects.all()
            data = []
            for student in students:
                data.append({
                    'ВУЗ': student.university,
                    'Факультет': student.faculty,
                    'Курс': student.course,
                    'ФИО': f"{student.surname} {student.name} {student.fathername}",
                    'Комната': student.room.id if student.room else None
                })
            
        elif report_type == 'checkin':
            # Экспорт отчета по срокам проживания
            students = CheckInInformation.objects.all()
            data = []
            for student in students:
                duration = (student.check_out_date - student.check_in_date).days if student.check_out_date else None
                data.append({
                    'ФИО': f"{student.surname} {student.name} {student.fathername}",
                    'Дата заселения': student.check_in_date,
                    'Дата выселения': student.check_out_date,
                    'Длительность проживания (дни)': duration,
                    'Комната': student.room.id if student.room else None
                })
        
        else:
            return Response(
                {'error': 'Неверный тип отчета'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Создание Excel файла
        df = pd.DataFrame(data)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Отчет', index=False)
        
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{report_type}_report.xlsx"'
        
        return response

class AllCheckInInformationListView(generics.ListAPIView):
    """
    Получение списка всей информации о заселении.
    """
    queryset = CheckInInformation.objects.all()
    serializer_class = CheckInInformationSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получение списка всей информации о заселении",
        responses={200: CheckInInformationSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class CheckInInformationAssignView(generics.GenericAPIView):
    """
    Привязка информации о заселении к комнате.
    """
    serializer_class = CheckInInformationAssignSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Привязка информации о заселении к комнате",
        request_body=CheckInInformationAssignSerializer,
        responses={
            200: "Успешное заселение",
            400: "Неверные данные",
            404: "Не найдено"
        }
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            check_in = serializer.validated_data['check_in']
            room = serializer.validated_data['room']
            
            check_in.room = room
            check_in.save()
            
            room.occupied_seats += 1
            room.save()
            
            return Response({
                'message': 'Студент успешно заселен в комнату',
                'data': CheckInInformationSerializer(check_in).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckInInformationUnassignView(generics.GenericAPIView):
    """
    Удаление информации о заселении из комнаты.
    """
    serializer_class = CheckInInformationAssignSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Удаление информации о заселении из комнаты",
        request_body=CheckInInformationAssignSerializer,
        responses={
            200: "Успешное выселение",
            400: "Неверные данные",
            404: "Не найдено"
        }
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            check_in = serializer.validated_data['check_in']
            room = serializer.validated_data['room']
            
            if check_in.room != room:
                return Response(
                    {'error': 'Студент не заселен в указанную комнату'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            check_in.room = None
            check_in.save()
            
            room.occupied_seats -= 1
            room.save()
            
            return Response({
                'message': 'Студент успешно выселен из комнаты',
                'data': CheckInInformationSerializer(check_in).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckInInformationWithoutRoomAndEmailCreateView(generics.CreateAPIView):
    """
    Создание информации о заселении без привязки к комнате и с автоматическим использованием email из токена.
    """
    queryset = CheckInInformation.objects.all()
    serializer_class = CheckInInformationWithoutRoomAndEmailSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Создание информации о заселении без привязки к комнате (email берется из токена)",
        request_body=CheckInInformationWithoutRoomAndEmailSerializer,
        responses={
            201: CheckInInformationWithoutRoomAndEmailSerializer,
            400: "Неверные данные"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'message': 'Информация о заселении успешно создана',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

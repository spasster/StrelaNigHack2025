from rest_framework import serializers
from .models import Room, CheckInInformation, Furniture
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Count, F

class CheckInInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckInInformation
        fields = [
            'id', 'room', 'name', 'surname', 'fathername',
            'phone_number', 'birth_date', 'university',
            'faculty', 'course', 'email', 'check_in_date',
            'check_out_date'
        ]
        read_only_fields = ['id']

    def validate(self, attrs):
        # Проверяем, существует ли пользователь с таким email
        User = get_user_model()
        email = attrs.get('email')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {'email': 'Пользователь с таким email не найден'}
            )
        
        # Проверяем наличие комнаты
        if 'room' not in attrs:
            raise serializers.ValidationError(
                {'room': 'Поле room является обязательным'}
            )
        
        return attrs

    def validate_room(self, room):
        # Проверяем, есть ли свободные места в комнате
        if room.occupied_seats >= room.seats:
            raise serializers.ValidationError("В комнате нет свободных мест")
        return room
        
class FurnitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furniture
        fields = ['id', 'type', 'count', 'room']
        read_only_fields = ['id']

    def validate_count(self, value):
        if value < 1:
            raise serializers.ValidationError("Количество мебели должно быть больше 0")
        return value

class RoomSerializer(serializers.ModelSerializer):
    available_seats = serializers.SerializerMethodField()
    furniture = FurnitureSerializer(many=True, read_only=True)
    check_ins = CheckInInformationSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'number', 'seats', 'occupied_seats', 'available_seats', 'gender', 'furniture', 'check_ins']

    def get_available_seats(self, obj):
        return obj.available_seats



class OccupancyReportSerializer(serializers.Serializer):
    total_rooms = serializers.IntegerField()
    occupied_rooms = serializers.IntegerField()
    free_rooms = serializers.IntegerField()
    occupancy_rate = serializers.FloatField()
    rooms_by_gender = serializers.DictField()

class UniversityReportSerializer(serializers.Serializer):
    university = serializers.CharField()
    total_students = serializers.IntegerField()
    faculties = serializers.DictField()
    courses = serializers.DictField()

class CheckInReportSerializer(serializers.Serializer):
    total_students = serializers.IntegerField()
    average_stay_duration = serializers.FloatField()
    students_by_duration = serializers.DictField()

class CheckInInformationWithoutRoomAndEmailSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), required=True)
    
    class Meta:
        model = CheckInInformation
        fields = [
            'id', 'room', 'name', 'surname', 'fathername',
            'phone_number', 'birth_date', 'university',
            'faculty', 'course', 'check_in_date',
            'check_out_date'
        ]
        read_only_fields = ['id']

    def validate(self, attrs):
        # Проверяем, что пользователь аутентифицирован
        if not self.context['request'].user.is_authenticated:
            raise serializers.ValidationError(
                {'error': 'Пользователь не аутентифицирован'}
            )
        
        # Проверяем наличие комнаты
        if 'room' not in attrs:
            raise serializers.ValidationError(
                {'room': 'Поле room является обязательным'}
            )
        
        return attrs

    def create(self, validated_data):
        # Добавляем email из токена
        validated_data['email'] = self.context['request'].user.email
        return super().create(validated_data)

class CheckInInformationAssignSerializer(serializers.Serializer):
    check_in_id = serializers.IntegerField()
    room_id = serializers.IntegerField()

    def validate(self, attrs):
        try:
            check_in = CheckInInformation.objects.get(id=attrs['check_in_id'])
            room = Room.objects.get(id=attrs['room_id'])
            
            if check_in.room:
                raise serializers.ValidationError(
                    {'error': 'Этот студент уже заселен в комнату'}
                )
            
            if room.occupied_seats >= room.seats:
                raise serializers.ValidationError(
                    {'error': 'В комнате нет свободных мест'}
                )
            
            attrs['check_in'] = check_in
            attrs['room'] = room
            return attrs
            
        except CheckInInformation.DoesNotExist:
            raise serializers.ValidationError(
                {'error': 'Информация о заселении не найдена'}
            )
        except Room.DoesNotExist:
            raise serializers.ValidationError(
                {'error': 'Комната не найдена'}
            ) 
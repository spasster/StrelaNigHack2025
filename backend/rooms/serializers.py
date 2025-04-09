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
        
        return attrs

    def validate_room(self, room):
        # Проверяем, есть ли свободные места в комнате
        if room.occupied_seats >= room.seats:
            raise serializers.ValidationError("В комнате нет свободных мест")
        return room
        
class FurnitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furniture
        fields = ['id', 'type', 'room']
        read_only_fields = ['id']

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

class CheckInInformationWithoutRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckInInformation
        fields = [
            'id', 'name', 'surname', 'fathername',
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
        
        return attrs

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
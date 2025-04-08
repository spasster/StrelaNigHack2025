from rest_framework import serializers
from .models import Room, CheckInInformation, Furniture
from django.db import models

class FurnitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furniture
        fields = ['id', 'type', 'room']
        read_only_fields = ['id']

class RoomSerializer(serializers.ModelSerializer):
    available_seats = serializers.SerializerMethodField()
    furniture = FurnitureSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'seats', 'occupied_seats', 'available_seats', 'gender', 'furniture']

    def get_available_seats(self, obj):
        return obj.available_seats

class CheckInInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckInInformation
        fields = [
            'id', 'name', 'surname', 'fathername',
            'phone_number', 'birth_date', 'university',
            'faculty', 'course'
        ]

    def validate(self, attrs):
        # Получаем все необходимые данные
        course = attrs.get('course')
        university = attrs.get('university')
        gender = 'F' if attrs.get('gender') == 'female' else 'M'

        # Ищем подходящую комнату
        suitable_rooms = Room.objects.filter(
            gender=gender
        ).exclude(occupied_seats__gte=models.F('seats'))

        if not suitable_rooms.exists():
            raise serializers.ValidationError("Нет подходящих комнат")

        # Проверяем каждую комнату на соответствие критериям
        for room in suitable_rooms:
            residents = CheckInInformation.objects.filter(room=room)
            if not residents.exists():
                # Если комната пустая, она подходит
                attrs['room'] = room
                return attrs

            # Проверяем курс и университет
            is_suitable = True
            for resident in residents:
                if abs(resident.course - course) > 1:
                    is_suitable = False
                    break
                if resident.university != university:
                    is_suitable = False
                    break

            if is_suitable:
                attrs['room'] = room
                return attrs

        raise serializers.ValidationError("Нет подходящих комнат по критериям") 
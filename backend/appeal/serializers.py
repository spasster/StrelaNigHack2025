from rest_framework import serializers
from .models import Appeal, AppealImage

class AppealImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppealImage
        fields = ['id', 'image', 'uploaded_at']

class AppealSerializer(serializers.ModelSerializer):
    images = AppealImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Appeal
        fields = ['id', 'user', 'category', 'description', 'status', 
                 'created_at', 'updated_at', 'images']
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class AppealStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appeal
        fields = ['status']
        
    def validate_status(self, value):
        if value not in ['pending', 'in_progress', 'completed']:
            raise serializers.ValidationError("Неверный статус обращения")
        return value 
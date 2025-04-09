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
        fields = ['id', 'user', 'category', 'description', 'image_base64', 
                 'status', 'created_at', 'updated_at', 'images']
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class AppealStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['pending', 'in_progress', 'completed'])
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance 
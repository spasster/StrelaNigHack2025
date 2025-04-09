from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Appeal, AppealImage
from .serializers import AppealSerializer, AppealStatusSerializer, AppealImageSerializer
from django.shortcuts import get_object_or_404

# Create your views here.

class AppealViewSet(viewsets.ModelViewSet):
    serializer_class = AppealSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Appeal.objects.all()
        return Appeal.objects.filter(user=self.request.user)
    
    def perform_destroy(self, instance):
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("Вы не можете удалить это обращение")
        instance.delete()
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        appeal = self.get_object()
        if not request.user.is_staff:
            return Response(
                {"detail": "У вас нет прав для изменения статуса"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = AppealStatusSerializer(appeal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def add_image(self, request, pk=None):
        appeal = self.get_object()
        if appeal.user != request.user:
            return Response(
                {"detail": "Вы не можете добавлять изображения к этому обращению"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = AppealImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(appeal=appeal)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

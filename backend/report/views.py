from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
from django.conf import settings
import os
from .models import Report
from .serializers import ReportSerializer
from .generators import ReportGenerator
import tempfile
from datetime import datetime

# Create your views here.

class ReportViewSet(viewsets.ViewSet):
    def create(self, request):
        report_type = request.data.get('report_type')
        format = request.data.get('format', 'XLSX')
        
        generator = ReportGenerator()
        if report_type == 'ROOM_OCCUPANCY':
            report = generator.generate_room_occupancy_report(format)
        elif report_type == 'STUDENT_DISTRIBUTION':
            report = generator.generate_student_distribution_report(format)
        elif report_type == 'STAY_DURATION':
            report = generator.generate_stay_duration_report(format)
        else:
            return Response(
                {'error': 'Неверный тип отчета'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создаем временный файл
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{format.lower()}') as tmp:
            if format == 'XLSX':
                report.save(tmp.name)
            else:  # DOCX
                report.save(tmp.name)

            # Читаем файл и отправляем его
            with open(tmp.name, 'rb') as f:
                response = FileResponse(
                    f,
                    as_attachment=True,
                    filename=f'report_{report_type}_{format.lower()}'
                )
            
            # Удаляем временный файл
            os.unlink(tmp.name)
            
            return response

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        report = self.get_object()
        file_path = os.path.join(settings.MEDIA_ROOT, report.file.name)
        
        if not os.path.exists(file_path):
            return Response(
                {'error': 'Файл не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        response = FileResponse(
            open(file_path, 'rb'),
            as_attachment=True,
            filename=os.path.basename(file_path)
        )
        return response

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Appeal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('in_progress', 'В работе'),
        ('completed', 'Выполнено'),
    ]
    
    CATEGORY_CHOICES = [
        ('electricity', 'Электрика'),
        ('plumbing', 'Сантехника'),
        ('furniture', 'Мебель'),
        ('other', 'Другое'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appeals')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image_base64 = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Обращение #{self.id} - {self.get_category_display()}"

class AppealImage(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='appeal_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Изображение для обращения #{self.appeal.id}"

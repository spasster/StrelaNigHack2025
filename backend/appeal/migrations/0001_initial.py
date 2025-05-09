# Generated by Django 5.2 on 2025-04-09 13:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('electricity', 'Электрика'), ('plumbing', 'Сантехника'), ('furniture', 'Мебель'), ('other', 'Другое')], max_length=20)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'В ожидании'), ('in_progress', 'В работе'), ('completed', 'Выполнено')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appeals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AppealImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='appeal_images/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('appeal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='appeal.appeal')),
            ],
        ),
    ]

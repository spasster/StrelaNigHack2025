# Generated by Django 5.2 on 2025-04-08 20:27

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats', models.PositiveIntegerField(verbose_name='Количество мест')),
                ('occupied_seats', models.PositiveIntegerField(default=0, verbose_name='Занятые места')),
                ('gender', models.CharField(choices=[('M', 'Мужская'), ('F', 'Женская')], max_length=1, verbose_name='Пол')),
            ],
            options={
                'verbose_name': 'Комната',
                'verbose_name_plural': 'Комнаты',
            },
        ),
        migrations.CreateModel(
            name='Furniture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100, verbose_name='Тип мебели')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='furniture', to='rooms.room', verbose_name='Комната')),
            ],
            options={
                'verbose_name': 'Мебель',
                'verbose_name_plural': 'Мебель',
            },
        ),
        migrations.CreateModel(
            name='CheckInInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('surname', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('fathername', models.CharField(max_length=100, verbose_name='Отчество')),
                ('phone_number', models.CharField(max_length=20, unique=True, verbose_name='Номер телефона')),
                ('birth_date', models.DateField(verbose_name='Дата рождения')),
                ('university', models.CharField(max_length=200, verbose_name='Университет')),
                ('faculty', models.CharField(max_length=200, verbose_name='Факультет')),
                ('course', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(6)], verbose_name='Курс')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email пользователя')),
                ('check_in_date', models.DateTimeField(verbose_name='Дата заселения')),
                ('check_out_date', models.DateTimeField(verbose_name='Дата выселения')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='check_ins', to='rooms.room', verbose_name='Комната')),
            ],
            options={
                'verbose_name': 'Информация о заселении',
                'verbose_name_plural': 'Информация о заселении',
            },
        ),
    ]

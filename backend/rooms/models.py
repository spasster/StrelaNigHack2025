from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Room(models.Model):
    number = models.CharField(max_length=10, verbose_name='Номер комнаты', unique=True)
    seats = models.PositiveIntegerField(verbose_name='Количество мест')
    occupied_seats = models.PositiveIntegerField(
        verbose_name='Занятые места',
        default=0
    )
    gender = models.CharField(
        max_length=1,
        choices=[('M', 'Мужская'), ('F', 'Женская')],
        verbose_name='Пол'
    )

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return f"Комната {self.number} ({self.gender})"

    @property
    def available_seats(self):
        return self.seats - self.occupied_seats

    def add_occupant(self):
        if self.occupied_seats < self.seats:
            self.occupied_seats += 1
            self.save()
            return True
        return False

    def remove_occupant(self):
        if self.occupied_seats > 0:
            self.occupied_seats -= 1
            self.save()
            return True
        return False

class Furniture(models.Model):
    type = models.CharField(max_length=100, verbose_name='Тип мебели')
    count = models.PositiveIntegerField(default=1, verbose_name='Количество')
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='furniture',
        verbose_name='Комната',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Мебель'
        verbose_name_plural = 'Мебель'

    def __str__(self):
        return f"{self.type} (x{self.count}) в комнате {self.room.id}"

    def move_to_room(self, new_room):
        """Перемещает мебель в другую комнату"""
        self.room = new_room
        self.save()

    def remove_from_room(self):
        """Удаляет мебель из комнаты"""
        self.delete()

class CheckInInformation(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='check_ins',
        verbose_name='Комната'
    )
    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    fathername = models.CharField(max_length=100, verbose_name='Отчество')
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Номер телефона'
    )
    birth_date = models.DateField(verbose_name='Дата рождения')
    university = models.CharField(max_length=200, verbose_name='Университет')
    faculty = models.CharField(max_length=200, verbose_name='Факультет')
    course = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        verbose_name='Курс'
    )
    email = models.EmailField(verbose_name='Email пользователя', unique=True)
    check_in_date = models.DateTimeField(verbose_name='Дата заселения')
    check_out_date = models.DateTimeField(verbose_name='Дата выселения')

    class Meta:
        verbose_name = 'Информация о заселении'
        verbose_name_plural = 'Информация о заселении'

    def __str__(self):
        return f"{self.surname} {self.name} {self.fathername}"

    @classmethod
    def get_user_info(cls, email):
        """Получение информации о заселении по email пользователя"""
        try:
            return cls.objects.get(email=email)
        except cls.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        if not self.pk:  # Если это новый объект
            if not self.room.add_occupant():
                raise ValueError("В комнате нет свободных мест")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.room.remove_occupant()
        super().delete(*args, **kwargs)

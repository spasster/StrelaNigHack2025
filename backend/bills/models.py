from django.db import models
from rooms.models import CheckInInformation
from datetime import datetime, timedelta

class Bill(models.Model):
    resident = models.ForeignKey(CheckInInformation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateTimeField(null=True, blank=True)
    bill_type = models.CharField(max_length=50, choices=[
        ('RENT', 'Аренда'),
        ('UTILITIES', 'Коммунальные услуги'),
        ('SUBSCRIPTION', 'Подписка'),
        ('OTHER', 'Прочее')
    ])
    subscription_period = models.CharField(max_length=20, choices=[
        ('MONTH', 'Месяц'),
        ('SEMESTER', 'Семестр'),
        ('YEAR', 'Год')
    ], null=True, blank=True)
    rent_start_date = models.DateField(null=True, blank=True)
    rent_end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Ожидает оплаты'),
        ('PAID', 'Оплачен'),
        ('OVERDUE', 'Просрочен'),
        ('CANCELLED', 'Отменён')
    ], default='PENDING')

    def __str__(self):
        return f"Счет #{self.id} - {self.resident} - {self.amount}"

    def save(self, *args, **kwargs):
        if self.bill_type == 'RENT' and self.rent_start_date and not self.rent_end_date:
            if self.subscription_period == 'MONTH':
                self.rent_end_date = self.rent_start_date + timedelta(days=30)
            elif self.subscription_period == 'SEMESTER':
                self.rent_end_date = self.rent_start_date + timedelta(days=180)
            elif self.subscription_period == 'YEAR':
                self.rent_end_date = self.rent_start_date + timedelta(days=365)
        super().save(*args, **kwargs)

class Payment(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=[
        ('CARD', 'Банковская карта'),
        ('CASH', 'Наличные'),
        ('TRANSFER', 'Банковский перевод')
    ])
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[
        ('SUCCESS', 'Успешно'),
        ('PENDING', 'В обработке'),
        ('FAILED', 'Ошибка')
    ])

    def __str__(self):
        return f"Платеж #{self.id} - {self.bill} - {self.amount}"

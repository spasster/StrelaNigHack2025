from django.db import models
from rooms.models import CheckInInformation

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
        ('OTHER', 'Прочее')
    ])
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Ожидает оплаты'),
        ('PAID', 'Оплачен'),
        ('OVERDUE', 'Просрочен'),
        ('CANCELLED', 'Отменён')
    ], default='PENDING')

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

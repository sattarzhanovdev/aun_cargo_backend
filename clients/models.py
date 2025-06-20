from django.db import models
from django.utils.timezone import now
from decimal import Decimal
from django.core.validators import MinValueValidator
# models.py
from django.db import models, transaction
from django.db.models import F
from django.utils.timezone import now
from django.core.exceptions import ValidationError



class Stock(models.Model):
    id = models.CharField(max_length=100, unique=True, primary_key=True)
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.FloatField(default=0)
    
    ORDER_STATUSES = [
        ('Приехал', 'Приехал'),
        ('На складе', 'На складе'),
        ('Передан', 'Передан')
    ]
    order_status = models.CharField(
        max_length=20, choices=ORDER_STATUSES, default='in_stock'
    )
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Transaction(models.Model):
    TYPE_CHOICES = (
        ('income', 'Доход'),
        ('expense', 'Расход'),
    )

    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.type} — {self.amount} на {self.date}"
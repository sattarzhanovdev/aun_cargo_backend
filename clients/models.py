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
    code = models.CharField(max_length=100, unique=True)
    client_id = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=255)
    weight = models.FloatField(default=0)

    ORDER_STATUSES = [
        ('Заказ принят', 'Заказ принят'),
        ('В пути', 'В пути'),
        ('В Кыргызстане', 'В Кыргызстане'),
        ('Товар получен', 'Товар получен')
    ]
    order_status = models.CharField(
        max_length=20, choices=ORDER_STATUSES, default='Заказ принят'
    )
    
    PAYMENT_STATUSES = [
        ('Не оплачен', 'Не оплачен'),
        ('Наличными', 'Наличными'),
        ('Оплачен картой', 'Оплачен картой')
    ]
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUSES, default='Не оплачен'
    )

    def __str__(self):
        return f"{self.code}"

    @property
    def price(self):
        return round(self.weight * 2.6 * 90, 2)  # 2 знака после запятой


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
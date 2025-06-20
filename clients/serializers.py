from rest_framework import serializers
from .models import (
    Stock, Transaction
)

class StockShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'code', 'name', 'price', 'order_status']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'name', 'date', 'type', 'amount']
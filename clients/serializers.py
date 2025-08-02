from rest_framework import serializers
from .models import (
    Stock, Transaction
)

class StockShortSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = ['id', 'code', 'client_id', 'weight', 'price', 'order_status']

    def get_price(self, obj):
        return obj.price  # ← это вызовет @property price

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'name', 'date', 'type', 'amount']
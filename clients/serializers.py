from rest_framework import serializers
from .models import (
    Stock, Transaction
)

class StockShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'name', 'date', 'type', 'amount']
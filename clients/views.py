from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta
from django.shortcuts import get_object_or_404

from .models import (
    Stock, Transaction
)
from .serializers import (
    StockShortSerializer, TransactionSerializer
)



from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class StockSummaryViewSet(viewsets.ModelViewSet):
    """
    • GET  — список товаров
    • POST — один или несколько
    • PUT  — обновление одного или нескольких
    """
    queryset = Stock.objects.all().order_by('name')
    serializer_class = StockShortSerializer

    # ------- POST -------
    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
            serializer.is_valid(raise_exception=True)   
            self.perform_bulk_create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return super().create(request, *args, **kwargs)

    def perform_bulk_create(self, validated_data_list):
        objs = [Stock(**data) for data in validated_data_list]
        Stock.objects.bulk_create(objs)

    # ------- PUT -------
    def update(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            updated_items = []
            for item in data:
                obj_id = item.get("id")
                if not obj_id:
                    continue
                instance = get_object_or_404(Stock, id=obj_id)
                serializer = self.get_serializer(instance, data=item, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                updated_items.append(serializer.data)
            return Response(updated_items, status=status.HTTP_200_OK)
        return super().update(request, *args, **kwargs)

    # ------- GET by-code/<code> -------
    @action(detail=False, methods=['get'], url_path='by-code/(?P<code>[^/.]+)')
    def by_code(self, request, code=None):
        instance = get_object_or_404(Stock, code=code)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-date')
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_bulk_create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return super().create(request, *args, **kwargs)

    def perform_bulk_create(self, validated_data_list):
        objs = [Transaction(**item) for item in validated_data_list]
        Transaction.objects.bulk_create(objs)
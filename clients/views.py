from datetime import timedelta
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Stock, Transaction
from .serializers import StockShortSerializer, TransactionSerializer


class StockSummaryViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с товарами (Stock):
    • GET  — список товаров
    • POST — создание одного или нескольких
    • PUT  — обновление одного или нескольких
    • GET /by-code/<code>/ — получить товар по коду
    """
    queryset = Stock.objects.all().order_by('-created_at')
    serializer_class = StockShortSerializer

    # === Bulk Create ===
    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_bulk_create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return super().create(request, *args, **kwargs)

    def perform_bulk_create(self, validated_data_list):
        # убираем вычисляемое поле price (оно property)
        objs = [Stock(**{k: v for k, v in data.items() if k != 'price'}) for data in validated_data_list]
        Stock.objects.bulk_create(objs)

    # === Bulk Update ===
    def update(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            updated_items = []
            with transaction.atomic():  # добавляем atomic, чтобы всё либо прошло, либо откатилось
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

    # === Получение по коду ===
    @action(detail=False, methods=['get'], url_path='by-code/(?P<code>[^/.]+)')
    def by_code(self, request, code=None):
        instance = get_object_or_404(Stock, code=code)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='status')
    def change_status(self, request, pk=None):
        """
        Обновляет статус заказа (order_status) по ID.
        Пример: POST /api/stocks/30/status { "status": "В пути" }
        """
        instance = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Stock.ORDER_STATUSES):
            return Response(
                {"detail": "Неверный статус."},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.order_status = new_status
        instance.save(update_fields=['order_status', 'updated_at'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet для учёта доходов и расходов:
    • GET  — список
    • POST — один или несколько
    """
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

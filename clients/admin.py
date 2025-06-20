from django.contrib import admin
from .models import (
    Stock
)

admin.register(Stock, 'stock')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'price', 'quantity', 'order_status')
    search_fields = ('code', 'name')
    list_filter = ('order_status',)
    ordering = ('-price',)

    def has_add_permission(self, request):
        return False
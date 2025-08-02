from django.contrib import admin
from .models import Stock

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('code', 'weight', 'client_id', 'price', 'order_status')  # ✅ убрали 'name'
    search_fields = ('code',)
    list_filter = ('order_status',)

    def has_add_permission(self, request):
        return False
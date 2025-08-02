from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'phone_number', 'client_id', 'pickUpPoint')
    search_fields = ('name', 'surname', 'phone_number', 'client_id')
    list_filter = ('pickUpPoint',)
    readonly_fields = ('client_id', 'warehouse')
from django.contrib import admin
from .models import Bill

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'grand_total', 'payment_method', 'is_paid', 'created_at']
    list_filter = ['is_paid', 'payment_method', 'created_at']
    search_fields = ['id', 'order__id']

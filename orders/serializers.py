from rest_framework import serializers
from .models import Order, OrderItem
from menu.models import MenuItem
from menu.serializers import MenuItemSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    item_details = MenuItemSerializer(source='item', read_only=True)
    subtotal = serializers.DecimalField(source='get_subtotal', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'item', 'item_details', 'quantity', 'price', 'subtotal']
        read_only_fields = ['price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    table_number = serializers.IntegerField(source='table.number', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'table', 'table_number', 'status', 'status_display', 'total_amount', 'created_at', 'updated_at', 'items']
        read_only_fields = ['total_amount', 'created_at', 'updated_at']

class AddOrderItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)

from rest_framework import serializers
from .models import Bill
from orders.serializers import OrderSerializer

class BillSerializer(serializers.ModelSerializer):
    order_details = OrderSerializer(source='order', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        model = Bill
        fields = [
            'id', 'order', 'order_details', 'tax', 'discount',
            'grand_total', 'payment_method', 'payment_method_display',
            'is_paid', 'created_at', 'paid_at'
        ]
        read_only_fields = ['grand_total', 'created_at', 'paid_at']

class GenerateBillSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    tax_percent = serializers.FloatField(default=5.0)
    discount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class PayBillSerializer(serializers.Serializer):
    payment_method = serializers.ChoiceField(choices=Bill.PaymentMethod.choices, default=Bill.PaymentMethod.CASH)

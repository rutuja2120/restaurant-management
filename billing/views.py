from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Bill
from orders.models import Order
from .serializers import BillSerializer, GenerateBillSerializer, PayBillSerializer

# Web Views
@login_required
def bill_list_view(request):
    bills = Bill.objects.select_related('order__table').all()
    return render(request, 'billing/bill_list.html', {'bills': bills})

@login_required
def bill_detail_view(request, pk):
    bill = get_object_or_404(Bill.objects.select_related('order__table').prefetch_related('order__items__item'), pk=pk)
    return render(request, 'billing/bill_detail.html', {'bill': bill})

@login_required
def generate_bill_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    bill, created = Bill.objects.get_or_create(order=order)
    bill.calculate_bill(tax_rate_percent=5.0, discount_amount=0.00)
    messages.success(request, f"Bill generated for Order #{order.id}.")
    return redirect('bill_detail', pk=bill.pk)

@login_required
def pay_bill_view(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'CASH')
        bill.mark_as_paid(payment_method=payment_method)
        messages.success(request, f"Bill #{bill.id} paid successfully via {bill.get_payment_method_display()}. Table is now free.")
        return redirect('bill_detail', pk=bill.pk)
    return redirect('bill_list')

# REST API ViewSet
class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['post'])
    def generate(self, request):
        serializer = GenerateBillSerializer(data=request.data)
        if serializer.is_valid():
            order = get_object_or_404(Order, pk=serializer.validated_data['order_id'])
            bill, created = Bill.objects.get_or_create(order=order)
            bill.calculate_bill(
                tax_rate_percent=serializer.validated_data['tax_percent'],
                discount_amount=serializer.validated_data['discount']
            )
            return Response(BillSerializer(bill).data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        bill = self.get_object()
        serializer = PayBillSerializer(data=request.data)
        if serializer.is_valid():
            bill.mark_as_paid(payment_method=serializer.validated_data['payment_method'])
            return Response(BillSerializer(bill).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

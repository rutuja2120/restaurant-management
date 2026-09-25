from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Order, OrderItem
from tables.models import Table
from menu.models import MenuItem
from .serializers import OrderSerializer, OrderItemSerializer, AddOrderItemSerializer

# Web Views
@login_required
def order_list_view(request):
    orders = Order.objects.select_related('table').prefetch_related('items__item').all()
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_create_view(request):
    tables = Table.objects.all()
    menu_items = MenuItem.objects.filter(is_available=True)

    if request.method == 'POST':
        table_id = request.POST.get('table_id')
        table = get_object_or_404(Table, pk=table_id)
        order = Order.objects.create(table=table)

        # Process menu items submitted in form
        for item in menu_items:
            qty = int(request.POST.get(f'item_{item.id}', 0))
            if qty > 0:
                order.add_item(item, qty)

        messages.success(request, f"Order #{order.id} created for Table {table.number}.")
        return redirect('order_list')

    return render(request, 'orders/order_create.html', {'tables': tables, 'menu_items': menu_items})

@login_required
def order_advance_status_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    old_status = order.get_status_display()
    new_status = order.advance_status()
    messages.success(request, f"Order #{order.id} status updated from {old_status} to {order.get_status_display()}.")
    return redirect('order_list')

# REST API ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        order = self.get_object()
        serializer = AddOrderItemSerializer(data=request.data)
        if serializer.is_valid():
            item = get_object_or_404(MenuItem, pk=serializer.validated_data['item_id'])
            quantity = serializer.validated_data['quantity']
            try:
                order_item = order.add_item(item, quantity)
                return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def advance(self, request, pk=None):
        order = self.get_object()
        order.advance_status()
        return Response(OrderSerializer(order).data)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer

from django.db.models import Q

# Web View
@login_required
def menu_list_view(request):
    query = request.GET.get('q', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    categories = Category.objects.prefetch_related('items').all()

    if query:
        categories = categories.filter(
            Q(name__icontains=query) | Q(items__name__icontains=query) | Q(items__description__icontains=query)
        ).distinct()

    return render(request, 'menu/menu_list.html', {
        'categories': categories,
        'query': query,
        'max_price': max_price
    })

@login_required
def toggle_item_availability_view(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    item.is_available = not item.is_available
    item.save()
    status_text = "Available" if item.is_available else "Unavailable"
    messages.success(request, f"Menu item '{item.name}' marked as {status_text}.")
    return redirect('menu_list')

# REST API ViewSets
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def toggle_availability(self, request, pk=None):
        item = self.get_object()
        item.is_available = not item.is_available
        item.save()
        return Response({'status': 'availability toggled', 'is_available': item.is_available})

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserRegistrationSerializer

User = get_user_model()

# Web Template Views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

@login_required
def dashboard_view(request):
    from tables.models import Table
    from orders.models import Order
    from billing.models import Bill
    from django.db.models import Sum

    total_tables = Table.objects.count()
    available_tables = Table.objects.filter(status=Table.Status.AVAILABLE).count()
    occupied_tables = Table.objects.filter(status=Table.Status.OCCUPIED).count()
    pending_orders = Order.objects.filter(status__in=[Order.Status.PENDING, Order.Status.PREPARING]).count()
    total_revenue = Bill.objects.filter(is_paid=True).aggregate(Sum('grand_total'))['grand_total__sum'] or 0.00

    context = {
        'total_tables': total_tables,
        'available_tables': available_tables,
        'occupied_tables': occupied_tables,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue,
        'recent_orders': Order.objects.select_related('table').order_by('-created_at')[:5]
    }
    return render(request, 'dashboard.html', context)


# REST API ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

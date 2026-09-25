from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.BillViewSet, basename='bill')

urlpatterns = [
    # Web UI URLs
    path('', views.bill_list_view, name='bill_list'),
    path('<int:pk>/', views.bill_detail_view, name='bill_detail'),
    path('generate/<int:order_id>/', views.generate_bill_view, name='generate_bill'),
    path('<int:pk>/pay/', views.pay_bill_view, name='pay_bill'),

    # API URLs
    path('api/', include(router.urls)),
]

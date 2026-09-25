from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.OrderViewSet, basename='order')

urlpatterns = [
    # Web UI URLs
    path('', views.order_list_view, name='order_list'),
    path('create/', views.order_create_view, name='order_create'),
    path('<int:pk>/advance/', views.order_advance_status_view, name='order_advance_status'),

    # API URLs
    path('api/', include(router.urls)),
]

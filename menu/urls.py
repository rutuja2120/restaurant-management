from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'items', views.MenuItemViewSet, basename='menuitem')

urlpatterns = [
    # Web UI URLs
    path('', views.menu_list_view, name='menu_list'),
    path('toggle/<int:pk>/', views.toggle_item_availability_view, name='toggle_menu_item'),

    # API URLs
    path('api/', include(router.urls)),
]

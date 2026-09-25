from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.TableViewSet, basename='table')

urlpatterns = [
    # Web UI URLs
    path('', views.table_list_view, name='table_list'),
    path('<int:pk>/status/<str:new_status>/', views.update_table_status_view, name='update_table_status'),

    # API URLs
    path('api/', include(router.urls)),
]

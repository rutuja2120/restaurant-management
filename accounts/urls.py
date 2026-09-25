from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    # Web UI URLs
    path('', views.dashboard_view, name='dashboard'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),

    # API URLs
    path('api/', include(router.urls)),
]

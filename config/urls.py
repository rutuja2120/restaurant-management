from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('tables/', include('tables.urls')),
    path('menu/', include('menu.urls')),
    path('orders/', include('orders.urls')),
    path('billing/', include('billing.urls')),

    # REST API Endpoints
    path('api/accounts/', include(('accounts.urls', 'accounts_api'), namespace='api_accounts')),
    path('api/tables/', include(('tables.urls', 'tables_api'), namespace='api_tables')),
    path('api/menu/', include(('menu.urls', 'menu_api'), namespace='api_menu')),
    path('api/orders/', include(('orders.urls', 'orders_api'), namespace='api_orders')),
    path('api/billing/', include(('billing.urls', 'billing_api'), namespace='api_billing')),
]

"""
URL configuration for inventory_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from inventory.views import (
    home,
    about,
    user_login,
    register_user,
    inventory_user,
    add_product,
    add_supplier,
    add_order,
    delete_product,
    delete_supplier,
    delete_order,
    logout_view,
    # API
    ProductListCreate, 
    SupplierListCreate, 
    OrderListCreate
) #importando las vistas

schema_view = get_schema_view(
    openapi.Info(
        title="Inventario API",
        default_version='v1',
        description="API para el sistema de inventario",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contacto@inventario.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('login/', user_login, name='login'),
    path('register/', register_user, name='register'),
    path('inventario/', inventory_user, name='inventario'),
    path('add_product/', add_product, name='add_product'),
    path('add_supplier/', add_supplier, name='add_supplier'),
    path('add_order/', add_order, name='add_order'),
    path('delete_product/<int:id>/', delete_product, name='delete_product'),
    path('delete_supplier/<int:id>/', delete_supplier, name='delete_supplier'),
    path('delete_order/<int:id>/', delete_order, name='delete_order'),
    path('logout/', logout_view, name='logout'),
    path('api/products/', ProductListCreate.as_view(), name='product-list'),
    path('api/suppliers/', SupplierListCreate.as_view(), name='supplier-list'),
    path('api/orders/', OrderListCreate.as_view(), name='order-list'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
]

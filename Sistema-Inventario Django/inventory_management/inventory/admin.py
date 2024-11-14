from django.contrib import admin
from .models import Product, Supplier, Order

# Register your models here.
admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(Order)


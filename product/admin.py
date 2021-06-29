from django.contrib import admin
from .models import Product, ProductCategory, Discount
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Discount)
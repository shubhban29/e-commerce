from django.db import models
from authen.models import User, Authmodel
# Create your models here.

class ProductCategory(Authmodel):
    name = models.CharField(max_length=30,null=True, blank=True)
    desc = models.TextField(max_length=255,null=True, blank=True)

class Discount(Authmodel):
    name = models.CharField(max_length=30,null=True, blank=True)
    desc = models.TextField(max_length=255,null=True, blank=True)
    discount_percent = models.FloatField(null=True, blank=True)
    active = models.BooleanField(default=False)

class Product(Authmodel):
    name = models.CharField(max_length=30,null=True, blank=True)
    desc = models.TextField(max_length=255,null=True, blank=True)
    SKU = models.CharField(max_length=20,null=True, blank=True)
    category_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    price = models.FloatField(null=True, blank=True)
    discount_id = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True, blank=True)
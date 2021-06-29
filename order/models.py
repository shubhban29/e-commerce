from django.db import models
from authen.models import User,Authmodel
from product.models import Product
# Create your models here.
STATUS_CHOICES = [
    ('completed','Complete'),
    ('failed','Failed'),
    ('pending','Pending'),
]
class Order(Authmodel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField(null=True,blank=True)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') 


class OrderItem(Authmodel):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(null=True, blank=True)


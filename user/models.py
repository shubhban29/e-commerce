from django.db import models
from authen.models import Authmodel, User
from product.models import Product
# Create your models here.

class UserAddress(Authmodel):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255, blank=True,null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=10, blank=True, null=True)
    mobile = models.CharField(max_length=10, blank=True, null=True)


class UserPayment(Authmodel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=100)
    provider = models.CharField(max_length=30, blank=True, null=True)
    card_on = models.CharField(max_length=16 , blank=True, null=True)
    expiry = models.DateField()
    card_holder_name = models.CharField(max_length=20)

class ShoppingSession(Authmodel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField(null=True, blank=True)

class CartItem(Authmodel):
    session_id = models.ForeignKey(ShoppingSession, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(null=True, blank=True)
STATUS_CHOICES = [
    ('PENDING','pending'),
    ('declined','declined'),
    ('complete','complete'),
]

class Payment(Authmodel):
    from order.models import Order
    amount = models.FloatField(null=True, blank=True)
    provider = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        order = Order.objects.get(pk=self.order_id)
        if status == 'complete':
            order.payment_status = 'complete'
        elif status == 'declined':
            order.payment_status = 'pending'
        order.save()
        super(Payment, self).save(*args, **kwargs)

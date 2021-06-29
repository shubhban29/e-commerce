from rest_framework import serializers
from django.contrib. auth import get_user_model,authenticate
from django.contrib.auth.models import Permission
from .models import Order, OrderItem
from user.models import Payment
from django.contrib.auth import authenticate


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
    
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

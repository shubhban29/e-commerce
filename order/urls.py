from django.urls import path, include
from authen.views import ResourceAPIView, GetListView
from .views import CreateOrderView
from .models import Order, OrderItem
from user.models import Payment
from .serializers import OrderSerializer, OrderItemSerializer, PaymentSerializer
urlpatterns = [
    path('order/<int:pk>', ResourceAPIView.as_view(
        model = Order,
        resource_serializer = OrderSerializer
    )),
    path('order-list/<str:page>',GetListView.as_view(
        model = Order,
        resource_serializer = OrderSerializer
    )),
    path('order-item/<int:pk>', ResourceAPIView.as_view(
        model = OrderItem,
        resource_serializer = OrderItemSerializer
    )),
    path('order-item-list/<str:page>',GetListView.as_view(
        model = OrderItem,
        resource_serializer = OrderItemSerializer
    )),
    path('payment/<int:pk>', ResourceAPIView.as_view(
        model = Payment,
        resource_serializer = PaymentSerializer
    )),
    path('payment-list/<str:page>',GetListView.as_view(
        model = Payment,
        resource_serializer = PaymentSerializer
    )),
    path('create-order/',CreateOrderView.as_view())
]
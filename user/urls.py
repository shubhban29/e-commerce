from django.urls import path, include
from authen.views import ResourceAPIView, GetListView
from .models import UserAddress, UserPayment, ShoppingSession, CartItem
from .serializers import UserAddressSerializer, UserPaymentSerializer, ShoppingSessionSerializer, CartItemSerializer
urlpatterns = [
    path('user-address/<int:pk>', ResourceAPIView.as_view(
        model = UserAddress,
        resource_serializer = UserAddressSerializer
    )),
    path('user-address-list/<str:page>',GetListView.as_view(
        model = UserAddress,
        resource_serializer = UserAddressSerializer
    )),
    path('user-payment/<int:pk>', ResourceAPIView.as_view(
        model = UserPayment,
        resource_serializer = UserPaymentSerializer
    )),
    path('user-payment-list/<str:page>',GetListView.as_view(
        model = UserPayment,
        resource_serializer = UserPaymentSerializer
    )),
    path('shopping-session/<int:pk>', ResourceAPIView.as_view(
        model = ShoppingSession,
        resource_serializer = ShoppingSessionSerializer
    )),
    path('shopping-session-list/<str:page>',GetListView.as_view(
        model = ShoppingSession,
        resource_serializer = ShoppingSessionSerializer
    )),
    path('cart-item/<int:pk>', ResourceAPIView.as_view(
        model = CartItem,
        resource_serializer = CartItemSerializer
    )),
    path('cart-item-list/<str:page>',GetListView.as_view(
        model = CartItem,
        resource_serializer = CartItemSerializer
    ))
]
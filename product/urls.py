from django.urls import path, include
from authen.views import ResourceAPIView, GetListView
from .models import ProductCategory, Discount, Product
from .serializers import ProductCategorySerializer, DiscountSerializer, ProductSerializer
urlpatterns = [
    path('product-category/<int:pk>', ResourceAPIView.as_view(
        model = ProductCategory,
        resource_serializer = ProductCategorySerializer
    )),
    path('product-category-list/<str:page>',GetListView.as_view(
        model = ProductCategory,
        resource_serializer = ProductCategorySerializer
    )),
    path('discount/<int:pk>', ResourceAPIView.as_view(
        model = Discount,
        resource_serializer = DiscountSerializer
    )),
    path('discount-list/<str:page>',GetListView.as_view(
        model = Discount,
        resource_serializer = DiscountSerializer
    )),
    path('product/<int:pk>', ResourceAPIView.as_view(
        model = Product,
        resource_serializer = ProductSerializer
    )),
    path('product-list/<str:page>',GetListView.as_view(
        model = Product,
        resource_serializer = ProductSerializer
    ))
]
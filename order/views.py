from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from authen.models import User
from order.models import Order, OrderItem
# Create your views here.
def current_user_details(request):
    user = User.objects.get(email=request.user.email)
    return dict(
        user=user,
        user_id=user.id
    )


class CreateOrderView(APIView):
    def put(self,request, *args, **kwargs):
        data = request.data
        info = current_user_details(request)
        modified_by = info['user']
        created_by = info['user']
        user_id = info['user']
        total = data['total']
        order_ = Order.objects.create(
            created_by= created_by,
            modified_by= modified_by,
            user_id= user_id,
            total = total,
            payment_status='pending'
        )
        items_data = data['items']
        items = []
        for item_data in items_data:
            item = OrderItem(
            product_id_id = item_data['product_id'],
            quantity = item_data['quantity'],
            created_by= created_by,
            modified_by = modified_by,
            order_id = order_)
            items.append(item)
        OrderItem.objects.bulk_create(items)
        return Response({})
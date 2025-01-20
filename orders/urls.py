from django.urls import path # type: ignore
from orders.views import OrderView

urlpatterns=[
    path(
        'orders', 
        OrderView.as_view(), 
        name='orders'
    ),
    path(
        'orders/<int:order_id>', 
        OrderView.as_view(), 
        name='order-details'
    ),
]
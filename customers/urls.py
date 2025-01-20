from django.urls import path # type: ignore
from customers.views import CustomerView

urlpatterns=[
    path(
        'customers', 
        CustomerView.as_view(), 
        name='customers'
    ),
    path(
        'customers/<int:customer_id>', 
        CustomerView.as_view(), 
        name='customer-details'
    ),
]
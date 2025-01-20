from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from django.contrib.auth import get_user_model
from customers.customer_repo import CustomerRepository
from customers.models import Customer
from orders.models import Order # type: ignore



def create_customer_setup(self, user_model):

    """Customer creation test setup function"""
    
    test_customers = [
        {
            
            "phone_number": "+254748800714",
            "first_name": "Ouma",
            "last_name": "Arera",
            "email": "ouma@example.com",
            'customer_code': "Test123"
        },
        {
            "phone_number": "+254748800716",
            "first_name": "Rambung'",
            "last_name": "Fee",
            "email": "fee@example.com",
            'customer_code': "Test124"
        }
    ]
    
    self.customers = []
    for customer_data in test_customers:
        customer = user_model.objects.create(**customer_data)
        self.customers.append(customer)

     

def create_order(self, order_model):

    """Order creation test setup function"""
    
    test_orders = [
        {"item": "Test Item 1", "price": 400, "customer_code": "Test124", "order_number": "OD1239"  },
        {"item": "Test Item 2", "price": 500, "customer_code": "Test124", "order_number": "OD1238"  },
        {"item": "Test Item 3", "price": 700, "customer_code": "Test124", "order_number": "OD1237"  },

        {"item": "Test Item 1", "price": 400, "customer_code": "Test123", "order_number": "OD1236"  },
        {"item": "Test Item 2", "price": 500, "customer_code": "Test123", "order_number": "OD1235"  },
        {"item": "Test Item 3", "price": 700, "customer_code": "Test123", "order_number": "OD1234" },
    ]
    
    self.orders = []
    for order_data in test_orders:
        
        customer = CustomerRepository.get_customer_by_customer_code(
             customer_code=order_data.pop("customer_code")
        )
        
        order_data['customer'] = customer
        order = order_model.objects.create(**order_data)
        self.orders.append(order)




class GlobalAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Create a mock user
        cls.mock_user = get_user_model().objects.create_user(
            username="mockuser",
            email="mockuser@example.com",
            password="password123"
        )

        # Generate JWT token
        refresh = RefreshToken.for_user(cls.mock_user)
        cls.token = str(refresh.access_token)

        # Set up test data
        create_customer_setup(self=cls, user_model=Customer)
        create_order(self=cls, order_model=Order)

    def authenticate(self):
        """Add Authorization header for authenticated requests."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    
    # @classmethod
    # def setUpTestData(cls):
    #     # 1. Set up customers
    #     create_customer_setup(self=cls, user_model=Customer)
    #     # 3. Order setup
    #     create_order(self=cls, order_model=Order)
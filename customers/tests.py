from rest_framework import status  # type: ignore
from rest_framework.reverse import reverse  # type: ignore
from customer_project.test_setup import GlobalAPITestCase
import json
from urllib.parse import urlencode


class CustomerViewTests(GlobalAPITestCase):
    def test_create_customer_success(self):
        """Test creating a new customer successfully."""
        test_customer = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "phone_number": "+254748800717",
        }

        endpoint = reverse('customers')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(endpoint, test_customer, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_customer_invalid_data(self):
        """Test creating a customer with invalid data."""
        test_customer = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "com.example@johndoe", # Invalid email
            "phone_number": "748800717", # Invalid phone number
        }

        endpoint = reverse('customers')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(endpoint, test_customer, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_customer_by_id_success(self):
        """Test fetching a customer by valid customer ID."""
        endpoint = reverse('customer-details', kwargs={"customer_id": 1})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(endpoint, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_customer_by_invalid_id(self):
        """Test fetching a customer by invalid customer ID."""
        endpoint = reverse('customer-details', kwargs={"customer_id": 9999})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(endpoint, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_customers(self):
        """Test fetching all customers."""
        endpoint = reverse('customers')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(endpoint, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_customer_with_query_params(self):
        """Test fetching customers with query parameters."""
        endpoint = f"{reverse('customers')}?{urlencode({'customer_code':'Test124'})}"
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(endpoint, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_customer_success(self):
        """Test updating a customer successfully."""
        test_customer_update = {
            "first_name": "John Updated",
            "phone_number": "+254745800715",
        }
        endpoint = reverse('customer-details', kwargs={"customer_id": 1})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.put(endpoint, test_customer_update, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_customer_invalid_data(self):
        """Test updating a customer with invalid data."""
        test_customer_update = {
            "phone_number": "invalid-phone",
        }
        endpoint = reverse('customer-details', kwargs={"customer_id": 1})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.put(endpoint, test_customer_update, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_nonexistent_customer(self):
        """Test updating a customer that does not exist."""
        test_customer_update = {
            "name": "Nonexistent Customer",
        }
        endpoint = reverse('customer-details', kwargs={"customer_id": 9999})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.put(endpoint, test_customer_update, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_customer_success(self):
        """Test deleting a customer successfully."""
        endpoint = reverse('customer-details', kwargs={"customer_id": 1})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(endpoint, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_nonexistent_customer(self):
        """Test deleting a customer that does not exist."""
        endpoint = reverse('customer-details', kwargs={"customer_id": 9999})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(endpoint, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

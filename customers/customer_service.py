from customers.utils import generate_unique_customer_code
from customers.customer_repo import CustomerRepository




class CustomerService:
    """Handles the business logic for customer."""

    @staticmethod
    def create_customer(customer_data):
        """
        Creates a new customer in the database.
        """
        try:
            customer_data['customer_code'] = generate_unique_customer_code()
            new_customer = CustomerRepository.create_customer(customer_data=customer_data)
            return new_customer
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all_customers(query_params):
        """
        Fetches and returns all customers, optionally filtered by query parameters.
        """
        try:
            customers = CustomerRepository.get_all_customers()
            if "customer_code" in query_params:
                customers = customers.filter(customer_code=query_params["customer_code"])

            return customers
        except Exception as ex:
            raise ex

    @staticmethod
    def get_customer_by_id(customer_id):
        """
        Fetches details of a customer by ID.
        """
        try:
            return CustomerRepository.get_customer_by_id(customer_id=customer_id)
        except Exception as ex:
            raise ex

    @staticmethod
    def update_customer(customer_id, cusromer_data):
        """
        Updates the details of an existing customer.
        """
        try:
            updated_customer = CustomerRepository.update_customer(
                customer_id=customer_id, 
                customer_data=cusromer_data
            )
            return updated_customer
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_customer(customer_id):
        """
        Deletes a customer by ID.
        """
        try:
            return CustomerRepository.delete_customer(customer_id=customer_id)
        except Exception as ex:
            raise ex

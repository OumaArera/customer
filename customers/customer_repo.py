import logging
from django.db import IntegrityError, DatabaseError  # type: ignore
from django.core.exceptions import ValidationError, ObjectDoesNotExist  # type: ignore
from customer_project.db_exceptions import (
    NotFoundException,
    IntegrityException,
    QueryException,
    DataBaseException,
)
from customers.models import Customer

logger = logging.getLogger(__name__)

class CustomerRepository:
    """Handles data layer operations for the Customer model."""

    @staticmethod
    def create_customer(customer_data):
        """Creates a new customer in the database."""
        try:
            customer = Customer.create_customer(validated_data=customer_data)
            customer.full_clean()
            customer.save()
            return customer
        except ValidationError as ex:
            logger.error(f"Validation error while creating customer: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating customer: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create customer.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating customer: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating the customer.")

    @staticmethod
    def get_all_customers():
        """Fetches and returns all customers."""
        try:
            customers = Customer.objects.all()
            return customers
        except DatabaseError as ex:
            logger.error(f"Database error while fetching customers: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch customers.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching customers: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching customers.")

    @staticmethod
    def get_customer_by_id(customer_id):
        """Fetches details of a customer by their ID."""
        try:
            customer = Customer.objects.get(pk=customer_id)
            return customer
        except ObjectDoesNotExist:
            raise NotFoundException(entity_name=f"Customer with ID {customer_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching customer by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch customer by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching customer by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching customer by ID.")
        
    @staticmethod
    def get_customer_by_customer_code(customer_code):
        """Fetches details of a customer by their code."""
        try:
            customer = Customer.objects.get(customer_code=customer_code)
            return customer
        except ObjectDoesNotExist:
            raise NotFoundException(entity_name=f"Customer with code {customer_code}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching customer by code: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch customer by code.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching customer by code: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching customer by code.")

    @staticmethod
    def update_customer(customer_id, customer_data):
        """Updates details of an existing customer."""
        try:
            customer = CustomerRepository.get_customer_by_id(customer_id=customer_id)
            for field, value in customer_data.items():
                setattr(customer, field, value)
            customer.full_clean()
            customer.save()
            return customer
        except NotFoundException as ex:
            raise ex
        except ValidationError as ex:
            logger.error(f"Validation error while updating customer: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating customer: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update customer.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating customer: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating the customer.")

    @staticmethod
    def delete_customer(customer_id):
        """Deletes a customer record by their ID."""
        try:
            customer = CustomerRepository.get_customer_by_id(customer_id=customer_id)
            customer.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting customer: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting customer: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete customer.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting customer: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting the customer.")
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from rest_framework import status  # type: ignore

from customers.customer_service import CustomerService
from customers.serializers import CustomerDeserializer, CustomerSerializer, UpdateCustomerDeserializer

from customer_project.utils import validate_query_params, APIResponse

class CustomerView(APIView):
    """User view for handling Customer"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Handles creating a new customer."""
        # print(f"User: {request.user}")
        try:
            deserializer = CustomerDeserializer(data=request.data)
            if deserializer.is_valid():
                validated_data = deserializer.validated_data
                new_customer = CustomerService.create_customer(customer_data=validated_data)
                serialized_user = CustomerSerializer(instance=new_customer)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Customer created successfully",
                        data=serialized_user.data
                    ),
                    status=status.HTTP_201_CREATED
                )
            return Response(
                APIResponse.error(
                    code="99",
                    message="Validation failed",
                    error=deserializer.errors
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="An error occurred while creating the customer",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def get(self, request, customer_id=None):
        """Handles fetching customers."""
        try:
            if customer_id:
                customer = CustomerService.get_customer_by_id(customer_id=customer_id)
                serialized_customer = CustomerSerializer(instance=customer)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Customer fetched successfully",
                        data=serialized_customer.data
                    ),
                    status=status.HTTP_200_OK
                )
            else:
                query_params = validate_query_params(
                    query_params=request.query_params,
                    valid_query_params={"customer_code"}
                )
                customers = CustomerService.get_all_customers(query_params=query_params)
                serialized_customers = CustomerSerializer(customers, many=True)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Customer fetched successfully",
                        data=serialized_customers.data
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching customers",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def put(self, request, customer_id):
        """Handles updating a customer."""
        try:
            deserializer = UpdateCustomerDeserializer(data=request.data)
            if deserializer.is_valid():
                validated_data = deserializer.validated_data
                updated_customer = CustomerService.update_customer(
                    customer_id=customer_id, 
                    cusromer_data=validated_data
                )
                serialized_customer = CustomerSerializer(instance=updated_customer)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Customer updated successfully",
                        data=serialized_customer.data
                    ),
                    status=status.HTTP_200_OK
                )
            return Response(
                APIResponse.error(
                    code="99",
                    message="Validation failed",
                    error=deserializer.errors
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error updating customer",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def delete(self, request, customer_id):
        """Handles deleting a user."""
        try:
            if CustomerService.delete_customer(customer_id=customer_id):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Customer deleted successfully",
                        data={"customer_id": customer_id}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting customer",
                    error=str(ex)
                ),
                status=ex.status_code
            )

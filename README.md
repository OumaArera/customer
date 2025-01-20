# Customer Management

Customer Management is a Django-based project designed to handle authentication, customer management, and order processing. It features three main apps: `auth_service`, `customers`, and `orders`. This project implements a modular design using the Repository pattern and integrates external services such as Auth0 for authentication and Africa's Talking for SMS notifications.

## Features

### Apps Overview
1. **auth_service**
   - Handles authentication and authorization using Auth0.
   - Ensures all endpoints are protected via JWT tokens.

2. **customers**
   - Manages customer creation.
   - Generates unique customer codes for each customer.

3. **orders**
   - Handles order creation linked to customers.
   - Sends SMS notifications to customers via Africa's Talking upon order creation.

### Architecture
- **Model**: Defines database models.
- **Repository**: Manages interactions with the database.
- **Service**: Contains business logic.
- **View**: Handles HTTP requests and responses.

### Testing
- Test data for customers and orders is preloaded in `test_setup.py`.
- Tests run using an SQLite3 database.
- CI/CD is integrated using CircleCI.

## Requirements
- Python 3.8+
- Django 5.1+
- pip

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:OumaArera/customer.git
   cd customer-management
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Use `.env` file to set up variables like `AUTH0_DOMAIN`, `AUTH0_CLIENT_ID`, `AUTH0_CLIENT_SECRET`, `SMS_API_KEY`, `SMS_USERNAME`, and `SHORT_CODE`.

5. Run database migrations:
   ```bash
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Running Tests

Run the test suite to ensure everything is working:
```bash
python manage.py test
```
Tests use SQLite3 as the database and include setup data for customers and orders.

## API Endpoints

### Customers
- **POST `/customers/`**: Create a new customer.
- **GET `/customers/<customer_id>/`**: Retrieve a customer by ID.

### Orders
- **POST `/orders/`**: Create a new order.
- **GET `/orders/<order_id>/`**: Retrieve an order by ID.

> **Note**: All endpoints are protected and require a valid JWT token for access.

## External Services
1. **Auth0**: Used for user authentication and authorization.
2. **Africa's Talking**: Sends SMS notifications to customers upon order creation.

## Continuous Integration & Deployment
- **CircleCI** is used for CI/CD to ensure quality and consistency across builds.

## Developer
This project was developed by **John Ouma**.

## License
This project is open-source and available under the MIT License.


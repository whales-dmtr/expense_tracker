# Expense Tracker

## Python REST API to manage and track your expenses, built with FastAPI

This project is a simple and secure REST API that you can use to manage your expenses, track your spending, and find out what you spend the most money on. Here are some features included in this project:

* Password hashing system  
* Authorization and authentication with JWT tokens  
* Full CRUD operations to manage your expenses

## API Endpoints

### Authentication

*   `POST /login`: Authenticate a user and receive a JWT token.
*   `POST /register`: Register a new user.

### User

*   `GET /me`: Get details of the authenticated user. (Requires authentication)

### Expenses

*   `GET /expense/{expense_id}`: Retrieve a specific expense by ID. (Requires authentication)
*   `GET /expenses`: Retrieve all expenses for the authenticated user. (Requires authentication)
*   `POST /expense`: Create a new expense. (Requires authentication)
*   `PUT /expense/{expense_id}`: Update an existing expense by ID. (Requires authentication)
*   `DELETE /expense/{expense_id}`: Delete a specific expense by ID. (Requires authentication)

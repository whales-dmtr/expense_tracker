# Expense Tracker

## Python REST API to manage and track your expenses, built with FastAPI

This project is a simple and secure REST API that allows you to manage your expenses, track your spending, and identify where your money goes most often. Below are some of the main features:

- Password hashing system  
- Authorization and authentication with JWT tokens  
- Full CRUD operations to manage your expenses  
- Search expenses by description text  

---

## API Endpoints

### 🔐 Authentication

- `POST /login` — Authenticate a user and receive a JWT token.  
- `POST /register` — Register a new user.

### 👤 User

- `GET /me` — Get details of the authenticated user. *(Requires authentication)*

### 💸 Expenses

- `GET /expense/{expense_id}` — Retrieve a specific expense by ID. *(Requires authentication)*  
- `GET /expenses` — Retrieve all expenses for the authenticated user. *(Requires authentication)*  
- `POST /expense` — Create a new expense. *(Requires authentication)*  
- `PUT /expense/{expense_id}` — Update an existing expense by ID. *(Requires authentication)*  
- `DELETE /expense/{expense_id}` — Delete a specific expense by ID. *(Requires authentication)*  
- `GET /expenses/search?query=...` — Search expenses by words in their description. *(Requires authentication)*

---

## 📚 API Documentation

Interactive API documentation is available at:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)  
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

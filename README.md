# Expense Tracker

## Python REST API to managing and tracking your expenses, built with FastAPI

This project is a simple and secure REST API that allows you to manage your expenses, track your spending, and identify where your money goes most often. Below are some of the main features:

- Secure password hashing  
- JWT-based authentication and authorization  
- Full CRUD support for managing expenses  
- Search expenses by text or regular expressions


---

## API Endpoints

### 🔐 Authentication

- `POST /auth/login` — Authenticate a user and receive a JWT token.  
- `POST /auth/register` — Register a new user.

### 👤 User

- `GET /me` — Get details of the authenticated user. *(Requires authentication)*

### 💸 Expenses

- `GET /expense/{expense_id}` — Retrieve a specific expense by ID. *(Requires authentication)*  
- `GET /expenses` — Retrieve all expenses for the authenticated user. *(Requires authentication)*  
- `POST /expense` — Create a new expense. *(Requires authentication)*  
- `PUT /expense/{expense_id}` — Update an existing expense by ID. *(Requires authentication)*  
- `DELETE /expense/{expense_id}` — Delete a specific expense by ID. *(Requires authentication)*  
- `GET /expenses/search?query=...` — Search expenses by words in their description. *(Requires authentication)*
- `GET /expenses/search/regex?pattern=...&flags=...` - Search expenses by regular expression. *(Requires authentication)*

---

## 📚 API Documentation

Interactive documentation is available when the API is running locally:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)  
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

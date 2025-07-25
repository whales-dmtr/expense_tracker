# 💰 Expense Tracker

## REST API for managing and tracking your expenses 

This project provides a simple, secure, and extensible REST API to manage personal expenses.  
You can track your spending habits, store expenses, and search them with flexible filtering (including regex support).

---

## 🚀 Features

- 🔐 Secure password hashing  
- 🪪 JWT-based authentication and authorization  
- ✅ Full CRUD support for expenses  
- 🔍 Search expenses by text or regular expressions  
- 🗄️ Database migrations powered by Alembic  
- 🐳 Fully Dockerized environment  

---

## 🧪 Installation & Usage (Docker Compose)

### 1. Clone the reposity

```bash
git clone https://github.com/whales-dmtr/expense_tracker.git
cd expense_tracker
```

### 2. Create .env file

Copy the example .env.example or create manually:

```env
# .env
DB_NAME=expense_tracker
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10
```
### 3. Run with Docker Compose

```bash
docker-compose up 
```

----
## 📚 API Documentation

Interactive documentation available when the server is running:

- 🔹 Swagger UI: [link](http://localhost:8000/docs)  
- 🔹 ReDoc: [link](http://localhost:8000/redoc)

---

## 📦 API Endpoints Overview

### 🔐 Authentication

- `POST /auth/register` — Register a new user  
- `POST /auth/login` — Authenticate and receive JWT token  

### 👤 User

- `GET /me` — Retrieve authenticated user details  
- `DELETE /me` — Remove authenticated user and all his expenses

### 💸 Expenses

- `GET /expense/{expense_id}` — Get specific expense  
- `GET /expenses` — List all expenses  
- `POST /expense` — Add a new expense  
- `PUT /expense/{expense_id}` — Update an existing expense  
- `DELETE /expense/{expense_id}` — Delete an expense  
- `GET /expenses/search?query=...` — Search by text  
- `GET /expenses/search/regex?pattern=...&flags=...` — Search by regex  

## 🧩 Tech Stack

- **Backend**: Python, FastAPI
- **Database**: PostgreSQL
- **Auth**: JWT (JSON Web Tokens)  
- **Migrations**: Alembic  
- **Containerization**: Docker & Docker Compose  

## 🛠️ Development

To run the project locally, follow these steps:

```bash
# This project requires Python 3.13.5
# You can install it from the official Python website
# or using pyenv:
pyenv install 3.13.5

# Start the database
# The easiest way is to use Docker:
docker run --name some-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=expense_tracker -d -p 5432:5432 postgres

# If you don't have Docker installed,
# you'll need to install PostgreSQL manually and create the database

# Create a .env file
# Make sure you're in the root directory of the project

# If you used the Docker command above,
# you can simply copy the .env file mentioned in the Installation section

# If you created the database manually,
# copy the template from .env.example, fill in the values, and continue

# Create and activate a virtual environment
python3.13 -m venv venv
source venv/bin/activate

# Install dependencies
python3.13 -m pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start the application
uvicorn app.main:app --reload
```

## ✅ Running Tests

After adding or modifying a feature, **make sure to run tests** to verify that the application’s functionality is not broken.

### 1) Tests require a **separate test database**

You can create one using the following Docker command or set it up manually:

```bash
docker run --name test-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=expense_tracker_test -d -p 5433:5432 postgres
```

### 2) Create a `.env.test` file

Make sure you're in the root directory of the project.

```env
# .env.test
TEST_DB_URL=postgresql://postgres:postgres@localhost:5433/expense_tracker_test
```

You can modify this URL to match your environment or Docker test configuration.

### 3) Run the tests

Make sure the virtual environment is activated:

```bash
source venv/bin/activate
pytest
```

## 📝 License

MIT — do whatever you want but don’t blame me :)

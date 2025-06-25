# 💰 Expense Tracker

## Python REST API for managing and tracking your expenses — built with FastAPI, Docker, and Alembic

This project provides a simple, secure, and extensible REST API to manage personal expenses.  
You can track your spending habits, store expenses, and search them with flexible filtering (including regex support).

---

## 🚀 Features

- 🔐 Secure password hashing  
- 🪪 JWT-based authentication and authorization  
- ✅ Full CRUD support for expenses  
- 🔍 Search expenses by text or regular expressions  
- 🐳 Dockerized environment with auto-applied Alembic migrations  

---

## 🧪 Installation & Usage (Docker Compose)

### 1. Clone the repo

```bash
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker
```

### 2. Create .env file

Copy the example .env.example or create manually:

```env
# .env
DB_NAME=expense_tracker
DB_USER=mysuperuser
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10
```
### 3. Run with Docker Compose

```bash
docker-compose up --build
```

----
## 📚 API Documentation

Interactive documentation available when the server is running:

- 🔹 Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)  
- 🔹 ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

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

- **Backend**: FastAPI, Pydantic, SQLAlchemy  
- **Database**: PostgreSQL  
- **Auth**: JWT (JSON Web Tokens)  
- **Migrations**: Alembic  
- **Containerization**: Docker & Docker Compose  

## 🛠️ Development

For local development without Docker, install dependencies and run manually (but you need to have running database and .env file for it):

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start the application
uvicorn app.main:app --reload
```

## 📝 License

MIT — do whatever you want but don’t blame me :)

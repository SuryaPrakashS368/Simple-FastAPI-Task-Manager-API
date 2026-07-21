# FastAPI Task Manager API

A simple Project Management API built using **FastAPI**, **SQLAlchemy**, **SQLite**, and **JWT Authentication**.

## Features

- User Signup
- User Login with JWT Authentication
- Create, Update, View and Delete Projects
- Create, Update, View and Delete Tasks
- Role-Based Access Control (RBAC)
- Task Assignment
- Soft Delete
- Swagger API Documentation

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- JWT Authentication
- Uvicorn

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd FastAPI_Task_Manager
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

## API Documentation

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

## Authentication

### Signup

```
POST /auth/signup
```

### Login

```
POST /auth/login
```

After successful login, use the generated JWT token to access protected APIs.

## Project Structure

```
FastAPI_Task_Manager/
│
├── alembic/
│
├── app/
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── oauth2.py
│   ├── dependencies.py
│   ├── middleware.py
│   ├── exceptions.py
│   ├── main.py
│   │
│   └── routes/
│       ├── user.py
│       ├── projects.py
│       ├── task.py
│       ├── project_members.py
│       └── analytics.py
│
├── requirements.txt
└── README.md
```

## Author

**Surya Prakash S**
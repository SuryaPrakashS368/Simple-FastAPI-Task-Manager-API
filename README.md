# FastAPI Task Manager API with Authentication

## Overview

This project is a **Task Manager REST API** built with **FastAPI**. It implements **JWT-based Authentication and Authorization**, allowing users to securely manage their own tasks.

## Features

- User Registration
- User Login with JWT Authentication
- Password Hashing using bcrypt
- Protected Routes
- Create, Read, Update, and Delete Tasks
- User-specific Task Management
- SQLite Database with SQLAlchemy ORM
- Interactive Swagger API Documentation

## Technologies Used

- FastAPI
- Python
- SQLite
- SQLAlchemy
- Pydantic
- Passlib (bcrypt)
- Python-JOSE (JWT)
- Uvicorn

## Project Structure

```text
FastAPI_Task_Manager/
│
├── app/
│   ├── routes/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── database.py
│   ├── oauth2.py
│   └── utils.py
│
├── requirements.txt
├── README.md
└── taskmanager.db
```

## Installation

```bash
git clone <repository-url>

cd FastAPI_Task_Manager

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

## API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## API Endpoints

### Authentication

- `POST /auth/signup` – Register a new user
- `POST /auth/login` – Login and get JWT token
- `GET /auth/me` – Get current user

### Tasks

- `POST /tasks` – Create a task
- `GET /tasks` – Get all tasks
- `GET /tasks/{id}` – Get a task by ID
- `PUT /tasks/{id}` – Update a task
- `DELETE /tasks/{id}` – Delete a task

## Security

- JWT Authentication
- Password Hashing (bcrypt)
- User-specific Authorization
- Protected Task Endpoints

## Author

Surya Prakash S
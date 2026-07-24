# FastAPI Project Management API

A Project Management REST API built using **FastAPI**, **SQLAlchemy**, and **SQLite**. It includes JWT Authentication, Role-Based Access Control (RBAC), Project and Task Management, Activity Logs, Notifications, and Analytics.

## Features

- JWT Authentication
- Role-Based Access Control (Admin, Manager, Member)
- User Management
- Project Management
- Task Management
- Project Member Management
- Activity Logs
- Notifications
- Audit Logs
- Analytics
- Soft Delete for Projects and Tasks

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- Uvicorn

## Project Structure

```text
FastAPI_Task_Manager/
│
├── app/
│   ├── Crud/
│   │   ├── activity.py
│   │   ├── analytics.py
│   │   ├── auditLog.py
│   │   ├── notification.py
│   │   ├── project.py
│   │   ├── project_member.py
│   │   ├── task.py
│   │   └── user.py
│   │
│   ├── routes/
│   │   ├── activity.py
│   │   ├── analytics.py
│   │   ├── auth.py
│   │   ├── notification.py
│   │   ├── project_members.py
│   │   ├── projects.py
│   │   ├── task.py
│   │   └── user.py
│   │
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── oauth2.py
│   ├── utils.py
│   ├── dependencies.py
│   ├── middleware.py
│   └── main.py
│
├── alembic/
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository

```bash
git clone <your-repository-url>
cd FastAPI_Task_Manager
```

2. Create a virtual environment

```bash
python -m venv venv
```

3. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Run database migrations

```bash
alembic upgrade head
```

6. Start the server

```bash
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

## Author

**Surya Prakash S**
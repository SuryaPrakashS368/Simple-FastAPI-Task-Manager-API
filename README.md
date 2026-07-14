# Simple FastAPI Task Manager API

A simple REST API built using **FastAPI**, **SQLAlchemy**, and **SQLite** for managing tasks.

## Features

- Create a task
- Get all tasks
- Get a task by ID
- Update a task
- Delete a task

## Technologies Used

- Python 3.x
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn

## Installation

1. Clone the repository:

```bash
git clone https://github.com/SuryaPrakashS368/Simple-FastAPI-Task-Manager-API.git
```

2. Navigate to the project:

```bash
cd Simple-FastAPI-Task-Manager-API
```

3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate the virtual environment:

Windows:

```bash
venv\Scripts\activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Start the server:

```bash
uvicorn main:app --reload
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

## Author

Surya Prakash S
